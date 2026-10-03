# -*- coding: utf-8 -*-

# Copyright 2024-2026 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://turbo.cr/"""

from .lolisafe import LolisafeAlbumExtractor
from .. import text

BASE_PATTERN = (r"(?:https?://)?(?:"
                r"(?:www\.)?turbo(?:vid)?\.cr|"
                r"saint\d*\.(?:su|pk|cr|to))")


class TurboAlbumExtractor(LolisafeAlbumExtractor):
    """Extractor for turbo.cr albums"""
    category = "turbo"
    root = "https://turbo.cr"
    pattern = BASE_PATTERN + r"/a/([^/?#]+)"
    example = "https://turbo.cr/a/ID"

    def fetch_album(self, album_id):
        url = f"{self.root}/a/{album_id}"
        page = self.request(url).text
        extr = text.extract_from(page)
        title = extr("<h1 ", "<")
        descr = extr("<p ", "<")
        headers = {"Referer": url}

        files = list(self._extract_files(page, headers))
        return files, {
            "album_id"     : album_id,
            "album_name"   : text.unescape(title[title.find(">")+1:]),
            "description"  : text.unescape(descr[descr.find(">")+1:]),
            "album_size"   : sum(f.get("size") or 0 for f in files),
            "count"        : len(files),
            "_http_headers": headers,
        }

    def _extract_files(self, body, headers):
        tbody = text.extr(body, 'id="fileTbody"', "</tbody>")
        if tbody:
            for file in text.extract_iter(tbody, "<tr", "</tr>"):
                data_id = text.extr(file, 'data-id="', '"')
                if not data_id:
                    continue
                yield self._sign_file(
                    data_id, headers,
                    text.parse_int(text.extr(file, 'data-size="', '"')))
            return

        files_js = text.extr(body, "const FILES = [", "];")
        if files_js:
            for match in text.re(
                    r'id\s*:\s*"([^"]+)"\s*,\s*name\s*:\s*"([^"]+)"'
                    r'\s*,\s*size\s*:\s*(\d+)').finditer(files_js):
                data_id, name, size = match.groups()
                yield self._sign_file(
                    data_id, headers, text.parse_int(size), name)

    def _sign_file(self, data_id, headers, size=0, name=None):
        url = f"{self.root}/api/sign?v={data_id}"
        data = self.request_json(url, headers=headers)
        name = (name or data.get("original_filename") or
                data.get("filename"))
        return text.nameext_from_name(name, {
            "id"  : data_id,
            "file": data.get("url"),
            "size": size or text.parse_int(data.get("size")),
            "_http_headers": headers,
        })


class TurboMediaExtractor(TurboAlbumExtractor):
    """Extractor for turbo.cr media links"""
    subcategory = "media"
    directory_fmt = ("{category}",)
    pattern = BASE_PATTERN + r"/(?:embe)?[dv]/([^/?#]+)"
    example = "https://turbo.cr/embed/ID"

    def fetch_album(self, album_id):
        try:
            return (self._extract_file(album_id),), {
                "album_id"   : "",
                "album_name" : "",
                "album_size" : -1,
                "description": "",
                "count"      : 1,
            }
        except Exception as exc:
            self.log.error("%s: %s", exc.__class__.__name__, exc)
            return (), {}

    def _extract_file(self, data_id):
        url = f"{self.root}/d/{data_id}"
        headers = {"Referer": url}
        page = self.request(url).text
        size = text.extr(page, 'id="fileSizeBytes">', '<')
        date = ""
        if match := text.re(r"<span>(\d{4}-\d{2}-\d{2})</span>").search(page):
            date = match.group(1)

        url = f"{self.root}/api/sign?v={data_id}"
        data = self.request_json(url, headers=headers)
        name = data.get("original_filename") or data.get("filename")
        return text.nameext_from_name(name, {
            "id"  : data_id,
            "file": data.get("url"),
            "size": int(text.parse_float(size.replace("&#43;", "+"))),
            "date": self.parse_datetime_iso(date),
            "_http_headers": headers,
        })
