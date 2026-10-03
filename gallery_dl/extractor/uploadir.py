# -*- coding: utf-8 -*-

# Copyright 2022-2025 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://uploadir.com/"""

from .common import Extractor, Message
from .. import text, exception


class UploadirFileExtractor(Extractor):
    """Extractor for uploadir files"""
    category = "uploadir"
    subcategory = "file"
    root = "https://uploadir.com"
    filename_fmt = "{filename} ({id}).{extension}"
    archive_fmt = "{id}"
    pattern = r"(?:https?://)?uploadir\.com/(?:user/)?u(?:ploads)?/([^/?#]+)"
    example = "https://uploadir.com/u/ID"

    def __init__(self, match):
        Extractor.__init__(self, match)
        self.file_id = match[1]

    def items(self):
        url = f"{self.root}/u/{self.file_id}"
        response = self.request(url, method="HEAD", allow_redirects=False)

        if 300 <= response.status_code < 400:
            url = response.headers["Location"]
            page = self.request(url).text
            if "No Longer Exists" in page:
                raise exception.NotFoundError("file")
            extr = text.extract_from(page)

            name = text.unescape(extr("<h2>", "</h2>").strip())
            url = self.root + extr('class="form" action="', '"')
            token = extr('name="authenticity_token" value="', '"')

            data = text.nameext_from_url(name, {
                "_http_method": "POST",
                "_http_data"  : {
                    "authenticity_token": token,
                    "upload_id": self.file_id,
                },
            })

        else:
            hcd = response.headers.get("Content-Disposition") or ""
            if "filename" not in hcd:
                page = self.request(url).text
                if "No Longer Exists" in page:
                    raise exception.NotFoundError("file")
                extr = text.extract_from(page)
                name = text.unescape(extr("<h2>", "</h2>").strip())
                action = extr('class="form" action="', '"')
                if not action:
                    raise exception.NotFoundError("file")
                url = self.root + action
                token = extr('name="authenticity_token" value="', '"')
                data = text.nameext_from_url(name, {
                    "_http_method": "POST",
                    "_http_data"  : {
                        "authenticity_token": token,
                        "upload_id": self.file_id,
                    },
                })
            else:
                name = (hcd.partition("filename*=UTF-8''")[2] or
                        text.extr(hcd, 'filename="', '"') or
                        self.file_id)
                data = text.nameext_from_url(name)

        data["id"] = self.file_id
        yield Message.Directory, "", data
        yield Message.Url, url, data
