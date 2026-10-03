# -*- coding: utf-8 -*-

# Copyright 2014-2026 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""HTTP client backed by curl_cffi.

The public surface matches the parts of ``requests`` gallery-dl actually
uses: sessions, streaming responses, cookie jars that iterate
``http.cookiejar.Cookie`` objects, and callable auth handlers.
"""

import re
import warnings
from http.cookiejar import Cookie
from http.cookies import SimpleCookie
from urllib.parse import urlsplit, urlunsplit, urlencode

import curl_cffi.requests.cookies as _curl_cookies
import curl_cffi.requests.models as _curl_models
import curl_cffi.requests.session as _curl_session
from curl_cffi import CurlHttpVersion, CurlOpt, CurlSslVersion
from curl_cffi.requests import Session as _CurlSession
from curl_cffi.requests.exceptions import (
    ChunkedEncodingError,
    ConnectionError,
    ContentDecodingError,
    RequestException,
    Timeout,
)
from curl_cffi.requests.headers import Headers
from curl_cffi.utils import CurlCffiWarning

# print HTTP traffic when enabled from gallery_dl.__init__
DEBUG = False


class Cookies(_curl_cookies.Cookies):
    """Cookie jar that iterates like ``requests.RequestsCookieJar``.

    ``for cookie in jar`` yields ``Cookie`` objects. ``keys()``,
    ``values()``, ``items()``, and ``name in jar`` use cookie names.
    ``set()`` accepts the same fields as ``requests``' ``create_cookie``,
    including ``expires``.
    """

    def set(self, name, value, **kwargs):
        if value is None:
            self.delete(
                name, domain=kwargs.get("domain"), path=kwargs.get("path"))
            return None

        domain = kwargs.get("domain") or ""
        path = kwargs.get("path") or "/"
        secure = bool(kwargs.get("secure", False))
        expires = kwargs.get("expires", None)
        if expires in (0, "0"):
            expires = None
        elif expires is not None:
            expires = int(expires)

        if name.startswith("__Secure-") and not secure:
            secure = True
        elif name.startswith("__Host-") and (
                not secure or domain or path != "/"):
            secure = True
            domain = ""
            path = "/"

        cookie = Cookie(
            version=0,
            name=name,
            value=value,
            port=None,
            port_specified=False,
            domain=domain,
            domain_specified=bool(domain),
            domain_initial_dot=domain.startswith("."),
            path=path,
            path_specified=bool(path),
            secure=secure,
            expires=expires,
            discard=expires is None,
            comment=kwargs.get("comment"),
            comment_url=kwargs.get("comment_url"),
            rest=kwargs.get("rest") or {"HttpOnly": None},
            rfc2109=False,
        )
        self.set_cookie(cookie)
        return cookie

    def set_cookie(self, cookie):
        self.jar.set_cookie(cookie)

    def __iter__(self):
        return iter(self.jar)

    def __contains__(self, name):
        for cookie in self.jar:
            if cookie.name == name:
                return True
        return False

    def keys(self):
        return [cookie.name for cookie in self.jar]

    def values(self):
        return [cookie.value for cookie in self.jar]

    def items(self):
        return [(cookie.name, cookie.value) for cookie in self.jar]


# curl_cffi constructs jars and response cookies from these module globals
_curl_cookies.Cookies = Cookies
_curl_session.Cookies = Cookies
_curl_models.Cookies = Cookies


_LINK_RE = re.compile(r"\s*<([^>]*)>\s*(?:;\s*([^,]*))?")


def _parse_links(value):
    """Parse a ``Link`` header into ``{rel: {"url": ..., "rel": ...}}``."""
    links = {}
    if not value:
        return links
    for match in _LINK_RE.finditer(value):
        url, params = match.group(1), match.group(2) or ""
        parsed = {"url": url}
        rel = None
        for part in params.split(";"):
            part = part.strip()
            if not part or "=" not in part:
                continue
            key, val = part.split("=", 1)
            key = key.strip()
            val = val.strip().strip("\"'")
            parsed[key] = val
            if key.lower() == "rel":
                rel = val
        if rel:
            links.setdefault(rel, parsed)
    return links


def _load_set_cookies(cookies, headers):
    get_list = getattr(headers, "get_list", None)
    if get_list is not None:
        values = get_list("set-cookie")
    else:
        value = headers.get("set-cookie") if headers else None
        values = [value] if value else []
    for set_cookie in values:
        if not set_cookie:
            continue
        try:
            parsed = SimpleCookie()
            parsed.load(set_cookie)
        except Exception:
            continue
        for name, morsel in parsed.items():
            cookies.set(
                name,
                getattr(morsel, "coded_value", None) or morsel.value,
                domain=morsel["domain"] or "",
                path=morsel["path"] or "/",
                secure=bool(morsel["secure"]),
            )


class Response(_curl_models.Response):
    """curl_cffi response plus the ``requests`` attributes extractors use."""

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    @property
    def links(self):
        cached = getattr(self, "_links", None)
        if cached is None:
            header = self.headers.get("link") if self.headers is not None else None
            cached = self._links = _parse_links(header)
        return cached

    @property
    def apparent_encoding(self):
        return self.encoding

    @property
    def is_permanent_redirect(self):
        return ("location" in self.headers and
                self.status_code in (301, 308))


class _AuthRequest():
    """Minimal request object for ``requests``-style auth callables."""

    __slots__ = ("method", "url", "headers")

    def __init__(self, method, url, headers):
        self.method = method
        self.url = url
        self.headers = headers


def _header_value(value):
    if isinstance(value, bytes):
        return value.decode("latin-1")
    return value


def _omit_none_params(params):
    """Drop ``None`` query values, matching ``requests`` encoding."""
    if params is None or isinstance(params, (str, bytes)):
        return params
    if isinstance(params, dict):
        out = {}
        for key, value in params.items():
            if value is None:
                continue
            if isinstance(value, (list, tuple)):
                value = type(value)(item for item in value if item is not None)
            out[key] = value
        return out
    if isinstance(params, (list, tuple)):
        return [(key, value) for key, value in params if value is not None]
    return params


def _omit_none_mapping(mapping):
    """Drop ``None`` values from a dict-like mapping."""
    if mapping is None or isinstance(mapping, (str, bytes)):
        return mapping
    items = getattr(mapping, "items", None)
    if items is None:
        return mapping
    if isinstance(mapping, dict):
        return {key: value for key, value in mapping.items()
                if value is not None}
    try:
        for key, value in list(items()):
            if value is None:
                del mapping[key]
    except Exception:
        pass
    return mapping


def _sanitize_request_kwargs(kwargs):
    """Make curl_cffi accept the ``requests`` kwargs gallery-dl uses."""
    if "params" in kwargs:
        params = _omit_none_params(kwargs["params"])
        if params:
            kwargs["params"] = params
        else:
            kwargs.pop("params", None)
    if "headers" in kwargs:
        headers = _omit_none_mapping(kwargs["headers"])
        if headers:
            kwargs["headers"] = headers
        else:
            kwargs.pop("headers", None)
    data = kwargs.get("data")
    if isinstance(data, dict):
        kwargs["data"] = _omit_none_mapping(data)
    return kwargs


def _url_with_params(url, params):
    if not params:
        return url
    params = _omit_none_params(params)
    if not params:
        return url
    if isinstance(params, str):
        query = params
    elif isinstance(params, bytes):
        query = params.decode()
    else:
        query = urlencode(params, doseq=True)
    parts = urlsplit(url)
    if parts.query:
        query = parts.query + "&" + query
    return urlunsplit((parts.scheme, parts.netloc, parts.path,
                       query, parts.fragment))


def _split_ciphers(cipher_list):
    tls13 = []
    other = []
    for part in cipher_list.split(":"):
        if not part:
            continue
        if part.startswith("TLS_"):
            tls13.append(part)
        else:
            other.append(part)
    return ":".join(other), ":".join(tls13)


class Session(_CurlSession):
    """``curl_cffi`` session with callable auth and redirect cookie fixes."""

    def __init__(self, **kwargs):
        kwargs.setdefault("default_headers", False)
        kwargs.setdefault("response_class", Response)
        if DEBUG:
            kwargs["debug"] = True
        super().__init__(**kwargs)
        if not isinstance(self._cookies, Cookies):
            compat = Cookies()
            compat.jar = self._cookies.jar
            self._cookies = compat
        # Default header encoding is inferred as ascii, which then rejects
        # non-ASCII Referer / Location values (IDN tests, localized titles).
        try:
            self.headers.encoding = "utf-8"
        except Exception:
            pass

    def request(self, method, url, **kwargs):
        kwargs = _sanitize_request_kwargs(kwargs)
        method, url, kwargs, saved_auth = _prepare_auth(
            self, method, url, kwargs)
        try:
            try:
                response = super().request(method, url, **kwargs)
            except RequestException as exc:
                # HTTP/2 frames must not carry an HTTP/1 Upgrade header.
                # Some hosts still send `upgrade: h2`; retry over 1.1.
                if (
                    kwargs.get("http_version") is None and
                    "curl: (92)" in str(exc)
                ):
                    kwargs["http_version"] = CurlHttpVersion.V1_1
                    response = super().request(method, url, **kwargs)
                else:
                    raise
        finally:
            if saved_auth is not _UNSET:
                self.auth = saved_auth
        _finish_response(response)
        return response


class _Unset():
    __slots__ = ()


_UNSET = _Unset()


def _prepare_auth(session, method, url, kwargs):
    """Apply a ``requests``-style auth callable before curl sees the request.

    curl_cffi only accepts an HTTP basic-auth ``(username, password)`` tuple.
    OAuth 1.0 and ``HTTPBasicAuth`` are callables that set an
    ``Authorization`` header instead.
    """
    if "auth" in kwargs:
        auth = kwargs.pop("auth")
    else:
        auth = session.auth

    if auth is None or isinstance(auth, tuple):
        if auth is not None:
            kwargs["auth"] = auth
        return method, url, kwargs, _UNSET

    if not callable(auth):
        kwargs["auth"] = auth
        return method, url, kwargs, _UNSET

    params = kwargs.pop("params", None)
    if params:
        url = _url_with_params(url, params)

    headers = {}
    if extra := kwargs.get("headers"):
        if isinstance(extra, Headers):
            extra = dict(extra.items())
        headers.update(extra)
    prepared = _AuthRequest(method.upper() if method else method, url, headers)
    auth(prepared)
    kwargs["headers"] = {
        key: _header_value(value)
        for key, value in prepared.headers.items()
        if value is not None
    }
    # ``auth or self.auth`` inside curl_cffi would otherwise see the callable
    saved = session.auth
    session.auth = None
    return method, url, kwargs, saved


def _finish_response(response):
    """Copy ``Set-Cookie`` from redirect responses onto ``history`` cookies.

    curl_cffi records redirect headers but leaves ``history[].cookies`` empty.
    Several extractors read cookies off the redirect that set them.
    """
    for hist in response.history or ():
        if hist.cookies:
            continue
        if hist.headers:
            _load_set_cookies(hist.cookies, hist.headers)


def _curl_version_text():
    version = __import__("curl_cffi").__curl_version__
    if isinstance(version, bytes):
        return version.decode()
    return str(version)


_CURL_VERSION = _curl_version_text()
BROTLI = "brotli/" in _CURL_VERSION
ZSTD = "zstd/" in _CURL_VERSION


def _configure_warnings():
    from . import config
    action = config.getg("warnings", "default")
    if not action:
        return
    try:
        warnings.simplefilter(action, CurlCffiWarning)
    except Exception:
        pass


_configure_warnings()
del _configure_warnings
