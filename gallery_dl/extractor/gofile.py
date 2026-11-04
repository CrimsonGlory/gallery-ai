# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://gofile.io/"""

from .common import Extractor, Message
from .. import text
import hashlib
import time


# image/jpeg -> jpg so extensionless images match typical image filters
_MIME_EXT = {
    "image/jpeg"               : "jpg",
    "image/jpg"                : "jpg",
    "image/png"                : "png",
    "image/gif"                : "gif",
    "image/bmp"                : "bmp",
    "image/x-bmp"              : "bmp",
    "image/x-ms-bmp"           : "bmp",
    "image/webp"               : "webp",
    "image/avif"               : "avif",
    "image/heic"               : "heic",
    "image/heif"               : "heif",
    "image/svg+xml"            : "svg",
    "image/ico"                : "ico",
    "image/icon"               : "ico",
    "image/x-icon"             : "ico",
    "image/vnd.microsoft.icon" : "ico",
}


def _extension_from_mime(mimetype):
    """Return a filename extension for an image MIME type, or ''."""
    if not mimetype:
        return ""
    mtype = mimetype.partition(";")[0].strip().lower()
    if ext := _MIME_EXT.get(mtype):
        return ext
    if mtype.startswith("image/"):
        subtype = mtype.rsplit("/", 1)[-1]
        if subtype.isalpha() and 2 <= len(subtype) <= 8:
            return subtype
    return ""


class GofileFolderExtractor(Extractor):
    category = "gofile"
    subcategory = "folder"
    root = "https://gofile.io"
    directory_fmt = ("{category}", "{name} ({code})")
    archive_fmt = "{id}"
    pattern = r"(?:https?://)?(?:www\.)?gofile\.io/d/([^/?#]+)"
    example = "https://gofile.io/d/ID"

    def items(self):
        recursive = self.config("recursive", True)
        password = self.config("password")

        token = self.config("api-token")
        if not token:
            token = self.cache(self._create_account, _key=None)
        self.cookies.set("accountToken", token, domain=".gofile.io")
        self.api_token = token

        folder = self._get_content(self.groups[0], password)
        yield Message.Directory, "", folder

        if not folder.get("canAccess"):
            raise self.exc.AuthorizationError("Password required")

        if "children" in folder:
            contents = folder.pop("children").values()
        else:
            contents = (folder,)
            folder = None

        num = 0
        for content in contents:
            content["folder"] = folder

            if content["type"] == "file":
                num += 1
                content["num"] = num
                self._prepare_file(content)
                yield Message.Url, content["link"], content

            elif content["type"] == "folder":
                if recursive:
                    url = "https://gofile.io/d/" + content["id"]
                    content["_extractor"] = GofileFolderExtractor
                    yield Message.Queue, url, content
                else:
                    self.log.debug("Skipping subfolder '%s'", content["id"])
            else:
                self.log.debug("'%s' is of unknown type (%s)",
                               content.get("name"), content["type"])

    def _prepare_file(self, content):
        text.nameext_from_name(content["name"], content)
        if not content["extension"]:
            content["extension"] = _extension_from_mime(
                content.get("mimetype"))

    def request_api(self, endpoint, params=None, headers=None, method="GET"):
        response = self.request_json(
            "https://api.gofile.io" + endpoint,
            method=method, params=params, headers=headers)

        if response["status"] != "ok":
            if response["status"] == "error-notFound":
                raise self.exc.NotFoundError("content")
            if response["status"] == "error-passwordRequired":
                raise self.exc.AuthorizationError("Password required")
            raise self.exc.AbortExtraction(
                f"{endpoint} failed (Status: {response['status']})")

        return response["data"]

    def _create_account(self):
        self.log.debug("Creating temporary account")
        return self.request_api("/accounts", method="POST")["token"]

    def _generate_website_token(self, lang="en-US"):
        # https://gofile.io/dist/js/wt.obf.js
        data = (f"{self.session.headers['User-Agent']}::"
                f"{lang}::"
                f"{self.api_token}::"
                f"{int(time.time() / 14400)}::"
                f"{self.config('salt') or '12af056dacea0b'}")
        return hashlib.sha256(data.encode()).hexdigest()

    def _get_content(self, content_id, password=None):
        params = {
            "contentFilter": ""	,
            "page"         : "1",
            "pageSize"     : "1000",
            "sortField"    : "name",
            "sortDirection": "1",
            "password"     : None if password is None else
                             hashlib.sha256(password.encode()).hexdigest(),
        }
        headers = {
            "Authorization"  : "Bearer " + self.api_token,
            "X-Website-Token": self._generate_website_token("en-US"),
            "X-BL"           : "en-US",
        }
        return self.request_api("/contents/" + content_id, params, headers)
