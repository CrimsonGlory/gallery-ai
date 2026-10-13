#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2015-2026 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import os
import select
import signal
import sys
import time
import traceback
import unittest

import re
import json
import hashlib
import datetime
import collections

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gallery_dl import \
    extractor, util, job, config, exception, formatter  # noqa E402


RESULTS = os.environ.get("GDL_TEST_RESULTS")
if RESULTS:
    results = util.import_file(RESULTS)
else:
    from test import results


# temporary issues, etc.
BROKEN = {
}

CONFIG = {
    "cache": {
        "file": None,
    },
    "downloader": {
        "adjust-extensions": False,
        "part": False,
    },
    "extractor": {
        # tests assert original file URLs, not thumbnail fallbacks
        "kemono": {"original": True},
        "coomer": {"original": True},
        "deviantart": {"original": True},
    },
}


AUTH_REQUIRED = {
    "pixiv",
    "pixiv-novel",
    "nijie",
    "horne",
    "reddit",
    "seiga",
    "fantia",
    "instagram",
    "twitter",
    "poipiku",
    "facebook",
}

AUTH_KEYS = {
    "username",
    "cookies",
    "api-key",
    "client-id",
    "access-token",
    "refresh-token",
}

# Live-suite noise: WAF, missing credentials, DNS, TLS, and timeouts.
# 404 / NotFoundError stay visible so gone URLs can be marked #exception.
_ENV_HTTP = re.compile(
    r"'5\d\d |"
    r"'40[13] |"
    r"'429 |"
    r"\bRead timed out\b|"
    r"curl: \((6|7|28|35|60)\)|"
    r"\btimed out\b|"
    r"DNSError|ConnectionError|CertificateVerifyError|SSLError",
    re.I,
)
_ENV_ABORT = re.compile(
    r"\b(401|403|429|50[0-9])\b|"
    r"Cloudflare|DDoS-Guard|CAPTCHA|WAF|Bot check|challenge|"
    r"Rate limit|PersistedQueryNotFound",
    re.I,
)
_ENV_EXCEPTIONS = (
    exception.ChallengeError,
    exception.AuthorizationError,
    exception.AuthenticationError,
    json.JSONDecodeError,
    exception.HttpError,
    exception.AbortExtraction,
)


# One hung URL (rate-limit sleep, dead connection, ignored HTTP timeout)
# must not stall the rest of the live suite. GDL_TEST_TIMEOUT overrides
# this, in seconds; 0 or a negative value disables the limit.
_TEST_TIMEOUT = 10 * 60
# How long a test may keep running after the limit while it reports the
# timeout. Then the test process is killed.
_TIMEOUT_GRACE = 15

# Set in the forked test process so a test cannot fork again.
_FORK_CHILD = False
_ACTIVE_TIMEOUT = _TEST_TIMEOUT
_FORK_UNSAFE = None


class TestTimeout(BaseException):
    """A single live extractor test exceeded its time limit."""


class _RemoteError(Exception):
    """Carries a traceback captured in the forked test process."""

    def __str__(self):
        text = super().__str__()
        return ("\n" + text) if text else ""


class TestExtractorResults(unittest.TestCase):

    def setUp(self):
        setup_test_config()

    def tearDown(self):
        config.clear()

    @classmethod
    def setUpClass(cls):
        cls._skipped = []

    @classmethod
    def tearDownClass(cls):
        if cls._skipped:
            sys.stdout.write("\n\nSkipped tests:\n")
            for url, reason in cls._skipped:
                sys.stdout.write(f'- {url} ("{reason}")\n')

    def run(self, result=None):
        """Run one live test, aborting it after the per-test time limit."""
        timeout = _live_test_timeout()
        if _FORK_CHILD or not timeout or timeout <= 0:
            return super().run(result)
        if not hasattr(os, "fork") or _fork_unsafe():
            return _run_inprocess(self, result, timeout)
        return _run_limited(self, result, timeout)

    def assertRange(self, value, range, msg=None):
        if range.step > 1:
            self.assertIn(value, range, msg=msg)
        else:
            self.assertLessEqual(value, range.stop, msg=msg)
            self.assertGreaterEqual(value, range.start, msg=msg)

    def assertLogEqual(self, exp, out):
        level, name, message = out.split(":", 2)

        if isinstance(exp, str):
            return self.assertEqual(exp, message, "#log")

        self.assertEqual(exp[0].lower(), level.lower(), "#log/level")
        if len(exp) < 3:
            self.assertEqual(exp[1], message, "#log/message")
        else:
            self.assertEqual(exp[1], name   , "#log/name")
            self.assertEqual(exp[2], message, "#log/message")

    def assertLogsEqual(self, expected, output):
        if isinstance(expected, str):
            expected = {expected[1:]} if expected[0] == "~" else (expected,)

        if isinstance(expected, set):
            self.assertLessEqual(len(expected), len(output), "#log/count")
            for exp in expected:
                for out in output:
                    try:
                        self.assertLogEqual(exp, out)
                        break
                    except AssertionError:
                        pass
                else:
                    self.fail(f'#log/Unmatched "{exp}"')
        else:
            self.assertEqual(len(output), len(expected), "#log/count")
            for exp, out in zip(expected, output):
                self.assertLogEqual(exp, out)

    def _run_test(self, result):
        if result.get("#fail"):
            del result["#fail"]
            try:
                self._run_test(result)
            except AssertionError:
                return
            else:
                self.fail("Test did not fail")

        base, cat, sub = result_categories(result)
        result.pop("#comment", None)
        result.pop("#category", None)
        auth = result.pop("#auth", None)

        cls = result["#class"]
        if cls.__module__.startswith("gallery_dl.extractor."):
            extr_url = extractor.find(result["#url"])
        else:
            extr_url = extractor_find_external(result)
        self.assertIs(extr_url.__class__, cls, "extractor by URL/find")
        extr_cls = extr = cls.from_url(result["#url"])
        self.assertIs(extr_cls.__class__, cls, "extractor by cls.from_url()")
        self.assertIs(extr_cls.__class__, extr_url.__class__)

        if len(result) <= 2:
            return  # only matching

        skip = result.pop("#skip", False)
        if skip:
            return self._skipped.append((result["#url"], skip))

        if auth is None:
            auth = (cat in AUTH_REQUIRED)
        elif not auth:
            # auth explicitly disabled
            for key in AUTH_KEYS:
                config.set((), key, None)

        if auth and not self._has_auth(extr, auth):
            self._skipped.append((result["#url"], "no auth"))
            self.skipTest("no auth")

        if "#options" in result:
            for key, value in result["#options"].items():
                key = key.split(".")
                config.set(key[:-1], key[-1], value)
        if "#range" in result:
            config.set((), "file-range" , result["#range"])
            config.set((), "child-range", result["#range"])

        tjob = ResultJob(extr,
                         content=("#sha1_content" in result),
                         format=(result.get("#metadata") != "post"))

        if "#exception" in result:
            exc = result["#exception"]
            if isinstance(exc, str):
                exc, _, msg = exc.partition(":")
                exc = getattr(exception, exc, None)
            elif isinstance(exc, tuple):
                exc, msg = exc
            else:
                msg = ""
            try:
                if "#log" in result:
                    with self.assertRaises(exc, msg="#exception") as cm, \
                            self.assertLogs() as log_info:
                        tjob.run()
                    self.assertLogsEqual(result["#log"], log_info.output)
                else:
                    with self.assertRaises(exc, msg="#exception") as cm:
                        tjob.run()
            except TestTimeout as env_exc:
                self._skipped.append((result["#url"], str(env_exc)))
                self.skipTest(str(env_exc))
            except _ENV_EXCEPTIONS as env_exc:
                self._skip_environment(result["#url"], env_exc)
                raise
            if msg:
                self.assertEqual(str(cm.exception), msg, msg="#exception/msg")
            return

        try:
            if "#log" in result:
                with self.assertLogs() as log_info:
                    tjob.run()
            else:
                tjob.run()
        except exception.StopExtraction:
            pass
        except TestTimeout as env_exc:
            self._skipped.append((result["#url"], str(env_exc)))
            self.skipTest(str(env_exc))
        except _ENV_EXCEPTIONS as env_exc:
            self._skip_environment(result["#url"], env_exc)
            raise

        if "#log" in result:
            self.assertLogsEqual(result["#log"], log_info.output)

        if result.get("#archive", True):
            self.assertEqual(
                len(set(tjob.archive_list)),
                len(tjob.archive_list),
                msg="archive-id uniqueness")

        if tjob.queue:
            # test '_extractor' entries
            for url, kwdict in zip(tjob.url_list, tjob.kwdict_list):
                if "_extractor" in kwdict:
                    extr = kwdict["_extractor"].from_url(url)
                    if extr is None and not result.get("#extractor", True):
                        continue
                    self.assertIsInstance(extr, kwdict["_extractor"], msg=url)
                    self.assertEqual(extr.url, url)
        else:
            # test 'extension' entries
            for kwdict in tjob.kwdict_list:
                self.assertIn("extension", kwdict, msg="#extension")

        # test extraction results
        if "#sha1_url" in result:
            self.assertEqual(
                result["#sha1_url"],
                tjob.url_hash.hexdigest(),
                msg="#sha1_url")

        if "#sha1_content" in result:
            expected = result["#sha1_content"]
            digest = tjob.content_hash.hexdigest()
            if isinstance(expected, str):
                self.assertEqual(expected, digest, msg="#sha1_content")
            else:  # iterable
                self.assertIn(digest, expected, msg="#sha1_content")

        if "#sha1_metadata" in result:
            self.assertEqual(
                result["#sha1_metadata"],
                tjob.kwdict_hash.hexdigest(),
                "#sha1_metadata")

        if "#count" in result:
            count = result["#count"]
            len_urls = len(tjob.url_list)
            if isinstance(count, str):
                self.assertRegex(
                    count, r"^ *(==|!=|<|<=|>|>=) *\d+ *$", msg="#count")
                expr = f"{len_urls} {count}"
                self.assertTrue(eval(expr), msg=expr)
            elif isinstance(count, range):
                self.assertRange(len_urls, count, msg="#count")
            else:  # assume integer
                self.assertEqual(len_urls, count, msg="#count")

        if "#pattern" in result:
            self.assertGreater(len(tjob.url_list), 0, msg="#pattern")
            pattern = result["#pattern"]
            if isinstance(pattern, str):
                for url in tjob.url_list:
                    self.assertRegex(url, pattern, msg="#pattern")
            else:
                self.assertEqual(
                    len(tjob.url_list), len(pattern), msg="#pattern/count")
                for url, pat in zip(tjob.url_list, pattern):
                    self.assertRegex(url, pat, msg="#pattern")

        if "#results" in result:
            expected = result["#results"]
            if isinstance(expected, str):
                self.assertTrue(tjob.url_list, msg="#results")
                self.assertEqual(
                    tjob.url_list[0], expected, msg="#results")
            else:
                self.assertSequenceEqual(
                    tjob.url_list, expected, msg="#results")

        metadata = {k: v for k, v in result.items() if k[0] != "#"}
        if metadata:
            if result.get("#metadata") == "post":
                kwdicts = tjob.kwdict_post
            else:
                kwdicts = tjob.kwdict_list
            for kwdict in kwdicts:
                self._test_kwdict(kwdict, metadata)

    def _skip_environment(self, url, exc):
        """Skip a live test when the failure is site-side or credentials."""
        reason = None
        if isinstance(exc, exception.ChallengeError):
            reason = str(exc)
        elif isinstance(exc, exception.AuthRequired):
            reason = str(exc) or "auth required"
        elif isinstance(exc, exception.AuthenticationError):
            reason = str(exc) or "authentication failed"
        elif isinstance(exc, exception.AuthorizationError):
            reason = str(exc) or "authorization required"
        elif isinstance(exc, json.JSONDecodeError):
            reason = f"{exc.__class__.__name__}: {exc}"
        elif isinstance(exc, exception.HttpError):
            extra = str(exc)
            if _ENV_HTTP.search(extra):
                reason = extra
        elif isinstance(exc, exception.AbortExtraction):
            extra = str(exc)
            if _ENV_ABORT.search(extra):
                reason = extra
        if reason:
            self._skipped.append((url, reason))
            self.skipTest(reason)

    def _has_auth(self, extr, auth):
        if auth is True:
            auth = AUTH_KEYS

        if isinstance(auth, str):
            return extr.config(auth)
        if isinstance(auth, set):
            return any(self._has_auth(extr, a) for a in auth)
        if isinstance(auth, (tuple, list)):
            return all(self._has_auth(extr, k) for k in auth)

        self.fail(f"Invalid '#auth' value: {auth!r}")

    def _test_kwdict(self, kwdict, tests, parent=None):
        for key, test in tests.items():

            if key.startswith("?"):
                key = key[1:]
                if key not in kwdict:
                    continue

            if key.endswith("[*]"):
                key = key[:-3]
                subtest = True
            else:
                subtest = False

            path = f"{parent}.{key}" if parent else key

            if key.startswith("!"):
                self.assertNotIn(key[1:], kwdict, msg=path)
                continue

            self.assertIn(key, kwdict, msg=path)
            value = kwdict[key]

            if subtest:
                self.assertNotIsInstance(value, str, msg=path)
                for idx, item in enumerate(value):
                    subpath = f"{path}[{idx}]"
                    self._test_kwdict_value(item, test, subpath)
            else:
                self._test_kwdict_value(value, test, path)

    def _test_kwdict_value(self, value, test, path):
        if isinstance(test, dict):
            self._test_kwdict(value, test, path)
        elif isinstance(test, type):
            self.assertIsInstance(value, test, msg=path)
        elif isinstance(test, range):
            self.assertRange(value, test, msg=path)
        elif isinstance(test, set):
            if isinstance(value, list):
                value = tuple(value)
            for item in test:
                if isinstance(item, type) and isinstance(value, item) or \
                        value == item:
                    break
            else:
                v = type(value) if len(str(value)) > 64 else value
                self.fail(f"{v!r} not in {test}: {path}")
        elif isinstance(test, list):
            subtest = False
            for idx, item in enumerate(test):
                if isinstance(item, dict):
                    subtest = True
                    subpath = f"{path}[{idx}]"
                    try:
                        obj = value[idx]
                    except Exception as exc:
                        self.fail(f"'{exc.__class__.__name__}: {exc}' "
                                  f"when accessing {subpath}")
                    self._test_kwdict(obj, item, subpath)
            if not subtest:
                self.assertEqual(test, value, msg=path)
        elif isinstance(test, str):
            if test.startswith("re:"):
                self.assertIsInstance(value, str, msg=path)
                self.assertRegex(value, test[3:], msg=path)
            elif test.startswith("dt:"):
                self.assertIsInstance(value, datetime.datetime, msg=path)
                self.assertEqual(test[3:], str(value), msg=path)
            elif test.startswith("type:"):
                name = test[5:]
                if name == "datetime":
                    self.assertIsInstance(
                        value, datetime.datetime, msg=path)
                else:
                    self.assertEqual(
                        name, type(value).__name__, msg=path)
            elif test.startswith("len:"):
                cls, _, length = test[4:].rpartition(":")
                if cls:
                    self.assertEqual(
                        cls, type(value).__name__, msg=f"{path}/type")
                try:
                    len_value = len(value)
                except Exception:
                    len_value = 0
                    for _ in value:
                        len_value += 1
                self.assertEqual(int(length), len_value, msg=path)
            elif test.startswith("hash:"):
                digest = test[5:].lower()
                msg = f"{path} / {digest}"
                if digest == "md5":
                    self.assertRegex(value, r"^[0-9a-fA-F]{32}$", msg)
                elif digest == "sha1":
                    self.assertRegex(value, r"^[0-9a-fA-F]{40}$", msg)
                elif digest == "sha256":
                    self.assertRegex(value, r"^[0-9a-fA-F]{64}$", msg)
                elif digest == "sha512":
                    self.assertRegex(value, r"^[0-9a-fA-F]{128}$", msg)
            elif test.startswith("iso:"):
                iso = test[4:]
                if iso in ("dt", "datetime", "8601"):
                    msg = f"{path} / ISO 8601"
                    try:
                        dt = datetime.datetime.fromisoformat(value)
                    except Exception as exc:
                        self.fail(f"Invalid datetime '{value}': {exc} {msg}")
                    self.assertIsInstance(dt, datetime.datetime, msg=msg)
                elif iso in ("lang", "639", "639-1"):
                    msg = f"{path} / ISO 639-1"
                    self.assertIsInstance(value, str, msg=msg)
                    self.assertRegex(value, r"^[a-z]{2}(-\w+)?$", msg=msg)
                elif iso in ("uuid", "11578", "11578:1996", "4122"):
                    msg = f"{path} / ISO 11578:1996"
                    pat = (r"(?i)[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-"
                           r"[0-9a-f]{4}-[0-9a-f]{12}")
                    self.assertIsInstance(value, str, msg=msg)
                    self.assertRegex(value, pat, msg=msg)
                else:
                    self.fail(f"Unsupported ISO test '{test}'")
            else:
                if "\r" in value:
                    value = value.replace("\r", "")
                self.assertEqual(test, value, msg=path)
        else:
            self.assertEqual(test, value, msg=path)


class ResultJob(job.DownloadJob):
    """Generate test-results for extractor runs"""

    def __init__(self, url, parent=None, content=False, format=True):
        job.DownloadJob.__init__(self, url, parent)
        self.queue = False
        self.content = content

        self.format = format
        self.url_list = []
        self.url_hash = hashlib.sha1()
        self.kwdict_list = []
        self.kwdict_post = []
        self.kwdict_hash = hashlib.sha1()
        self.archive_list = []
        self.archive_hash = hashlib.sha1()
        self.content_hash = hashlib.sha1()

        if content:
            self.fileobj = TestPathfmt(self.content_hash)
        else:
            self._update_content = lambda url, kwdict: None

    def run(self):
        self._init()
        self.dispatch(self.extractor)

    def handle_url(self, url, kwdict, fallback=None):
        self._update_url(url)
        self._update_kwdict(kwdict)
        self._update_archive(kwdict)
        self._update_content(url, kwdict)
        self.format_filename(kwdict)

    def handle_directory(self, kwdict):
        if self.format is not None:
            if self.format:
                self.format_directory = TestFormatter(
                    "".join(self.extractor.directory_fmt)).format_map
                self.format_filename = TestFormatter(
                    self.extractor.filename_fmt).format_map
                self.format_archive = TestFormatter(
                    self.extractor.archive_fmt).format_map
            else:
                self.format_directory = \
                    self.format_filename = \
                    self.format_archive = lambda kwdict: ""
            self.format = None

        self._update_kwdict(kwdict, False)
        self.format_directory(kwdict)

    def handle_metadata(self, kwdict):
        pass

    def handle_queue(self, url, kwdict):
        self.queue = True
        self._update_url(url)
        self._update_kwdict(kwdict)

    def _update_url(self, url):
        self.url_list.append(url)
        self.url_hash.update(url.encode())

    def _update_kwdict(self, kwdict, to_list=True):
        if to_list:
            self.kwdict_list.append(kwdict.copy())
        else:
            self.kwdict_post.append(kwdict.copy())
        kwdict = util.filter_dict(kwdict)
        self.kwdict_hash.update(
            json.dumps(kwdict, sort_keys=True, default=str).encode())

    def _update_archive(self, kwdict):
        archive_id = self.format_archive(kwdict)
        self.archive_list.append(archive_id)
        self.archive_hash.update(archive_id.encode())

    def _update_content(self, url, kwdict):
        self.fileobj.kwdict = kwdict

        downloader = self.get_downloader(url.partition(":")[0])
        if downloader.download(url, self.fileobj):
            return

        for num, url in enumerate(kwdict.get("_fallback") or (), 1):
            self.log.warning("Trying fallback URL #%d", num)
            downloader = self.get_downloader(url.partition(":")[0])
            if downloader.download(url, self.fileobj):
                return


class TestPathfmt():

    def __init__(self, hashobj):
        self.hashobj = hashobj
        self.path = ""
        self.temppath = ""
        self.size = 0
        self.kwdict = {}
        self.extension = "jpg"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def open(self, mode):
        self.size = 0
        return self

    def write(self, content):
        """Update SHA1 hash"""
        self.size += len(content)
        self.hashobj.update(content)

    def tell(self):
        return self.size

    def part_size(self):
        return 0


class TestFormatter(formatter.StringFormatter):

    def _apply_simple(self, key, fmt):
        if key == "extension" or "_parse_optional." in repr(fmt):
            def wrap(obj):
                try:
                    return fmt(obj[key])
                except KeyError:
                    return ""
        elif "<function identity at " in repr(fmt):
            def wrap(obj):
                return "".join(obj[key])
        else:
            def wrap(obj):
                return fmt(obj[key])
        return wrap

    def _apply(self, key, funcs, fmt):
        if key == "extension" or "_parse_optional." in repr(fmt):
            def wrap(obj):
                if obj := obj.get(key):
                    for func in funcs:
                        obj = func(obj)
                else:
                    obj = ""
                return fmt(obj)
        elif "<function identity at " in repr(fmt):
            def wrap(obj):
                return "".join(obj[key])
        else:
            def wrap(obj):
                obj = obj[key]
                for func in funcs:
                    obj = func(obj)
                return fmt(obj)
        return wrap


def setup_test_config():
    config._config.update(CONFIG)


def load_test_config():
    try:
        path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "archive", "config.json")
        with open(path) as fp:
            CONFIG.update(json.loads(fp.read()))
    except FileNotFoundError:
        pass
    except Exception as exc:
        sys.exit(f"Error when loading {path}: {exc.__class__.__name__}: {exc}")


def extractor_find_external(result, imported=set()):
    _module_iter_orig = extractor._module_iter
    try:
        file = sys.modules[result["#class"].__module__].__file__
        if file not in imported:
            path, filename = os.path.split(file)
            extractor._module_iter = extractor._modules_path(path, (filename,))
            imported.add(file)
        return extractor.find(result["#url"])
    finally:
        extractor._module_iter = _module_iter_orig


def result_categories(result):
    categories = result.get("#category")
    if categories:
        return categories

    cls = result["#class"]
    return cls.basecategory, cls.category, cls.subcategory


def _live_test_timeout():
    raw = os.environ.get("GDL_TEST_TIMEOUT")
    if raw is None or raw == "":
        return _TEST_TIMEOUT
    try:
        return float(raw)
    except ValueError:
        sys.stderr.write(
            f"Invalid GDL_TEST_TIMEOUT={raw!r}; using {_TEST_TIMEOUT}s\n")
        return _TEST_TIMEOUT


def _format_timeout(seconds):
    seconds = float(seconds)
    if seconds >= 60 and seconds % 60 == 0:
        minutes = int(round(seconds // 60))
        unit = "minute" if minutes == 1 else "minutes"
        return f"individual test timed out after {minutes} {unit}"
    text = f"{seconds:g}"
    unit = "second" if text == "1" else "seconds"
    return f"individual test timed out after {text} {unit}"


def _timeout_handler(signum, frame):
    raise TestTimeout(_format_timeout(_ACTIVE_TIMEOUT))


def _arm_timeout(seconds):
    signal.signal(signal.SIGALRM, _timeout_handler)
    if hasattr(signal, "setitimer"):
        signal.setitimer(signal.ITIMER_REAL, seconds)
    else:
        signal.alarm(max(1, int(float(seconds) + 0.999)))


def _disarm_timeout():
    if hasattr(signal, "setitimer"):
        signal.setitimer(signal.ITIMER_REAL, 0)
    elif hasattr(signal, "alarm"):
        signal.alarm(0)
    # Drop a signal already queued so it cannot fire while the outcome
    # is written back to the parent.
    if hasattr(signal, "SIGALRM"):
        signal.signal(signal.SIGALRM, signal.SIG_IGN)


def _fork_unsafe():
    """os.fork() deadlocks if another thread is alive. Fall back then."""
    global _FORK_UNSAFE
    if _FORK_UNSAFE is None:
        try:
            import threading
            unsafe = threading.active_count() > 1
        except Exception:
            unsafe = True
        if unsafe:
            sys.stderr.write(
                "warning: live tests share this process; "
                "a hard hang may ignore the per-test timeout\n")
        _FORK_UNSAFE = unsafe
    return _FORK_UNSAFE


def _run_inprocess(case, result, timeout):
    """Best-effort limit where fork is unavailable."""
    global _ACTIVE_TIMEOUT
    if not hasattr(signal, "SIGALRM"):
        return super(TestExtractorResults, case).run(result)

    previous = signal.getsignal(signal.SIGALRM)
    _ACTIVE_TIMEOUT = timeout
    _arm_timeout(timeout)
    try:
        return super(TestExtractorResults, case).run(result)
    finally:
        _disarm_timeout()
        signal.signal(signal.SIGALRM, previous)


def _run_limited(case, result, timeout):
    if result is None:
        result = case.defaultTestResult()
        startTestRun = getattr(result, "startTestRun", None)
        stopTestRun = getattr(result, "stopTestRun", None)
        if startTestRun is not None:
            startTestRun()
    else:
        stopTestRun = None

    result.startTest(case)
    started = time.monotonic()
    try:
        _fork_test(case, result, timeout)
    finally:
        add_duration = getattr(result, "addDuration", None)
        if add_duration is not None:
            add_duration(case, time.monotonic() - started)
        result.stopTest(case)
        if stopTestRun is not None:
            stopTestRun()
    return result


def _fork_test(case, result, timeout):
    try:
        sys.stdout.flush()
        sys.stderr.flush()
    except Exception:
        pass

    read_fd, write_fd = os.pipe()
    try:
        pid = os.fork()
    except OSError as exc:
        os.close(read_fd)
        os.close(write_fd)
        _add_error(result, case, RuntimeError(
            f"failed to fork test process: {exc}"))
        return

    if pid == 0:
        os.close(read_fd)
        try:
            _child_main(case, write_fd, timeout)
        except BaseException:
            traceback.print_exc()
            _exit_child(1)
        _exit_child(1)

    grace = min(_TIMEOUT_GRACE, max(1.0, float(timeout)))
    deadline = time.monotonic() + float(timeout) + grace
    try:
        os.close(write_fd)
        write_fd = -1
        kind, data, status = _wait_child(pid, read_fd, deadline)
    finally:
        if write_fd >= 0:
            os.close(write_fd)
        os.close(read_fd)
        _reap_if_running(pid)

    if kind == "timeout":
        reason = _format_timeout(timeout)
        skipped = getattr(case.__class__, "_skipped", None)
        if skipped is not None:
            skipped.append(("", reason))
        result.addSkip(case, reason)
        return

    payload = None
    if data:
        try:
            payload = json.loads(data.decode())
        except (UnicodeDecodeError, json.JSONDecodeError):
            payload = None

    if status is not None and os.WIFSIGNALED(status):
        sig = os.WTERMSIG(status)
        if sig == signal.SIGINT:
            raise KeyboardInterrupt
        if payload is None:
            _add_error(result, case, RuntimeError(
                f"test process killed by signal {sig}"))
            return
    if status is not None and os.WIFEXITED(status):
        code = os.WEXITSTATUS(status)
        if code == 130:
            raise KeyboardInterrupt
        if code != 0 and payload is None:
            _add_error(result, case, RuntimeError(
                f"test process exited with status {code}"))
            return
    if payload is None:
        if data:
            detail = "unreadable test result"
        elif status is None:
            detail = "test process disappeared before reporting"
        else:
            detail = "test process produced no result"
        _add_error(result, case, RuntimeError(detail))
        return
    _apply_payload(case, result, payload)


def _child_main(case, write_fd, timeout):
    global _FORK_CHILD, _ACTIVE_TIMEOUT
    _FORK_CHILD = True
    _ACTIVE_TIMEOUT = timeout
    _die_with_parent()
    try:
        os.setsid()
    except OSError:
        pass
    try:
        sys.stdout.reconfigure(line_buffering=True)
        sys.stderr.reconfigure(line_buffering=True)
    except Exception:
        pass

    skipped = getattr(case.__class__, "_skipped", None)
    nskip = len(skipped) if skipped is not None else 0
    if hasattr(signal, "SIGALRM"):
        _arm_timeout(timeout)
    try:
        payload = _collect_outcome(case, nskip)
    except KeyboardInterrupt:
        _disarm_timeout()
        _exit_child(130)
    except BaseException:
        _disarm_timeout()
        payload = _error_payload(traceback.format_exc(), case, nskip)
    else:
        _disarm_timeout()

    try:
        sys.stdout.flush()
        sys.stderr.flush()
    except Exception:
        pass
    try:
        _write_all(write_fd, _dump_payload(payload))
        os.close(write_fd)
    except OSError:
        pass
    _exit_child(0)


def _collect_outcome(case, nskip):
    private = unittest.TestResult()
    # Call TestCase.run directly. TestExtractorResults.run would fork again.
    unittest.TestCase.run(case, private)
    return {
        "failures": [text for _, text in private.failures],
        "errors": [text for _, text in private.errors],
        "skipped": ["" if reason is None else str(reason)
                    for _, reason in private.skipped],
        "expected_failures": [text for _, text in private.expectedFailures],
        "unexpected_success": bool(private.unexpectedSuccesses),
        "skipped_extra": _new_skips(case.__class__, nskip),
    }


def _error_payload(text, case, nskip):
    return {
        "failures": [],
        "errors": [text],
        "skipped": [],
        "expected_failures": [],
        "unexpected_success": False,
        "skipped_extra": _new_skips(case.__class__, nskip),
    }


def _new_skips(cls, nskip):
    skipped = getattr(cls, "_skipped", None)
    if not skipped or len(skipped) <= nskip:
        return []
    extra = []
    for item in skipped[nskip:]:
        try:
            url, reason = item
        except (TypeError, ValueError):
            url, reason = item, ""
        extra.append([str(url), "" if reason is None else str(reason)])
    return extra


def _dump_payload(payload):
    try:
        return json.dumps(payload).encode()
    except (TypeError, ValueError):
        fallback = {
            "failures": [],
            "errors": ["failed to serialize the test outcome"],
            "skipped": [],
            "expected_failures": [],
            "unexpected_success": False,
            "skipped_extra": [],
        }
        return json.dumps(fallback).encode()


def _apply_payload(case, result, payload):
    extra = payload.get("skipped_extra") or []
    if isinstance(extra, list) and extra:
        rows = []
        for item in extra:
            if isinstance(item, (list, tuple)) and len(item) == 2:
                rows.append((item[0], item[1]))
        if rows:
            skipped = getattr(case.__class__, "_skipped", None)
            if skipped is None:
                case.__class__._skipped = rows
            else:
                skipped.extend(rows)

    reported = False
    if _report_formatted(
            result, case, payload.get("failures"),
            "addFailure", "failures"):
        reported = True
    if _report_formatted(
            result, case, payload.get("errors"),
            "addError", "errors"):
        reported = True
    for reason in payload.get("skipped") or []:
        if not isinstance(reason, str):
            reason = str(reason)
        result.addSkip(case, reason)
        reported = True
    if _report_formatted(
            result, case, payload.get("expected_failures"),
            "addExpectedFailure", "expectedFailures"):
        reported = True
    if payload.get("unexpected_success"):
        result.addUnexpectedSuccess(case)
        reported = True
    if not reported:
        result.addSuccess(case)


def _report_formatted(result, case, texts, add_name, bucket_name):
    """Record tracebacks captured in the child.

    addFailure/addError print the progress marker the active Python
    version expects. The stored text is then put back to the child's
    original traceback so the summary is not wrapped in a second
    exception.
    """
    if not isinstance(texts, list) or not texts:
        return False
    add = getattr(result, add_name, None)
    bucket = getattr(result, bucket_name, None)
    if add is None or bucket is None:
        _add_error(result, case, RuntimeError("\n".join(map(str, texts))))
        return True
    before = len(bucket)
    for text in texts:
        if not isinstance(text, str):
            text = str(text)
        add(case, _remote_exc_info(text))
    for offset, text in enumerate(texts):
        if not isinstance(text, str):
            text = str(text)
        if not text.endswith("\n"):
            text += "\n"
        index = before + offset
        if index < len(bucket):
            bucket[index] = (case, text)
    return True


def _remote_exc_info(text):
    return (_RemoteError, _RemoteError(text), None)


def _add_error(result, case, exc):
    result.addError(case, (type(exc), exc, None))


def _wait_child(pid, read_fd, deadline):
    """Wait until the child reports, the deadline passes, or it is killed.

    Returns ("exit"|"timeout", payload_bytes, wait_status).
    wait_status is None when the child was already reaped.
    """
    chunks = []
    sigints = 0
    status = None

    def poll():
        nonlocal status
        if status is not None:
            return True
        try:
            pid_done, current = os.waitpid(pid, os.WNOHANG)
        except ChildProcessError:
            return True
        if not pid_done:
            return False
        status = current
        return True

    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            _kill_tree(pid)
            if status is None:
                status = _reap(pid)
            return "timeout", b"", status

        try:
            readable, _, _ = select.select(
                [read_fd], [], [], min(remaining, 0.5))
        except KeyboardInterrupt:
            sigints += 1
            if sigints >= 2:
                _kill_tree(pid)
                if status is None:
                    _reap(pid)
                raise
            try:
                os.kill(pid, signal.SIGINT)
            except ProcessLookupError:
                pass
            continue

        if readable:
            try:
                data = os.read(read_fd, 65536)
            except InterruptedError:
                continue
            except OSError:
                data = b""
            if data:
                chunks.append(data)
                continue
            while status is None and time.monotonic() < deadline:
                if poll():
                    break
                time.sleep(0.05)
            if status is None:
                _kill_tree(pid)
                status = _reap(pid)
                return "timeout", b"", status
            return "exit", b"".join(chunks), status

        if poll():
            chunks.extend(_drain(read_fd))
            return "exit", b"".join(chunks), status


def _reap(pid):
    try:
        _pid, status = os.waitpid(pid, 0)
    except ChildProcessError:
        return None
    return status


def _reap_if_running(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return
    _kill_tree(pid)
    _reap(pid)


def _kill_tree(pid):
    try:
        pgid = os.getpgid(pid)
    except ProcessLookupError:
        return
    if pgid != os.getpgrp():
        try:
            os.killpg(pgid, signal.SIGKILL)
            return
        except ProcessLookupError:
            return
        except OSError:
            pass
    try:
        os.kill(pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def _drain(fd):
    chunks = []
    try:
        os.set_blocking(fd, False)
    except OSError:
        return chunks
    while True:
        try:
            data = os.read(fd, 65536)
        except BlockingIOError:
            break
        except OSError:
            break
        if not data:
            break
        chunks.append(data)
    return chunks


def _write_all(fd, data):
    view = memoryview(data)
    while view:
        written = os.write(fd, view)
        view = view[written:]


def _exit_child(code):
    # A normal timeout still has to reap subprocesses this test started
    # (yt-dlp, ffmpeg, ...). SIGKILL cannot be ignored, so skip our own pid.
    _kill_process_group_peers()
    try:
        sys.stdout.flush()
        sys.stderr.flush()
    except Exception:
        pass
    os._exit(code)


def _kill_process_group_peers():
    try:
        # Most tests never spawn anything. waitpid reports that without
        # walking /proc. A live or zombie child falls through to the sweep.
        try:
            waited, _status = os.waitpid(-1, os.WNOHANG)
        except ChildProcessError:
            return
        if waited:
            # Reap any further zombies, then still look for live peers.
            while True:
                try:
                    waited, _status = os.waitpid(-1, os.WNOHANG)
                except ChildProcessError:
                    break
                if not waited:
                    break
        mypid = os.getpid()
        pgid = os.getpgrp()
        for name in os.listdir("/proc"):
            if not name.isdigit():
                continue
            pid = int(name)
            if pid == mypid:
                continue
            try:
                with open(f"/proc/{pid}/stat", "rb") as fh:
                    stat = fh.read()
            except OSError:
                continue
            fields = stat[stat.rfind(b")") + 2:].split()
            try:
                pgrp = int(fields[2])
            except (IndexError, ValueError):
                continue
            if pgrp != pgid:
                continue
            try:
                os.kill(pid, signal.SIGKILL)
            except OSError:
                continue
            try:
                os.waitpid(pid, 0)
            except ChildProcessError:
                pass
    except Exception:
        pass


def _die_with_parent():
    """Kill this test if the suite process dies (Linux).

    The parent can itself be PID 1 (a container entrypoint), so compare
    against the pid captured before prctl rather than assuming init is 1.
    """
    try:
        import ctypes
        parent = os.getppid()
        libc = ctypes.CDLL(None, use_errno=True)
        # PR_SET_PDEATHSIG
        libc.prctl.argtypes = [
            ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong,
            ctypes.c_ulong, ctypes.c_ulong,
        ]
        libc.prctl.restype = ctypes.c_int
        if libc.prctl(1, signal.SIGKILL, 0, 0, 0) != 0:
            return
        if os.getppid() != parent:
            os._exit(1)
    except Exception:
        pass


def generate_tests():
    """Dynamically generate extractor unittests"""
    def _generate_method(result):
        def test(self):
            sys.stdout.write(f"\n{result['#url']}\n")
            if "#comment" in result:
                sys.stdout.write(f"# {result['#comment']}\n")

            try:
                self._run_test(result)
            except KeyboardInterrupt as exc:
                v = input("\n[e]xit | [f]ail | [S]kip ? ").strip().lower()
                if v in ("e", "exit"):
                    raise
                if v in ("f", "fail"):
                    self.fail("manual test failure")
                else:
                    self._skipped.append((result["#url"], "manual skip"))
                    self.skipTest(exc)
        return test

    # enable selective testing for direct calls
    if __name__ == "__main__" and len(sys.argv) > 1:
        category, _, subcategory = sys.argv[1].partition(":")
        del sys.argv[1:]

        if category.startswith("+"):
            basecategory = category[1:].lower()
            tests = [t for t in results.all()
                     if result_categories(t)[0].lower() == basecategory]
        else:
            tests = results.category(category)

        if subcategory:
            if subcategory.startswith("+"):
                url = subcategory[1:]
                tests = [t for t in tests if url in t["#url"]]
            elif subcategory.startswith("~"):
                com = subcategory[1:]
                tests = [t for t in tests
                         if "#comment" in t and com in t["#comment"].lower()]
            else:
                tests = [t for t in tests
                         if result_categories(t)[-1] == subcategory]
    else:
        tests = results.all()

    # add 'test_...' methods
    enum = collections.defaultdict(int)
    for result in tests:
        base, cat, sub = result_categories(result)
        name = f"{cat}_{sub}"
        enum[name] += 1

        method = _generate_method(result)
        method.__doc__ = result["#url"]
        method.__name__ = f"test_{name}_{enum[name]}"
        setattr(TestExtractorResults, method.__name__, method)


generate_tests()
if __name__ == "__main__":
    load_test_config()
    unittest.main(warnings="ignore")
