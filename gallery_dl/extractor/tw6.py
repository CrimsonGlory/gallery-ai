# -*- coding: utf-8 -*-

# Copyright 2026 Mike Fährmann

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://tw6.jp/"""

from .common import Extractor, Message
from .. import text

BASE_PATTERN = r"(?:https?://)?(?:www\.)?tw6\.jp/gallery"


class Tw6Extractor(Extractor):
    """Base class for tw6 extractors"""
    category = "tw6"
    root = "https://tw6.jp"
    directory_fmt = ("{category}", "{master_name}")
    filename_fmt = "{character_name}_{illust_id}.{extension}"
    archive_fmt = "{illust_id}"

    def items(self):
        for post in self.posts():
            url = post["image_url"]
            text.nameext_from_url(url, post)
            yield Message.Directory, "", post
            yield Message.Url, url, post

    def _pagination(self, params):
        url = self.root + "/api/illust_search"
        params["n"] = 0

        while True:
            data = self.request_json(url, params=params)

            if not data:
                break
            yield from data

            params["n"] += 1


class Tw6UserExtractor(Tw6Extractor):
    subcategory = "user"
    pattern = BASE_PATTERN + r"/master/?\?master_id=(\d+)"
    example = "https://tw6.jp/gallery/master/?master_id=12345"

    def posts(self):
        self.kwdict["master_id"] = master_id = self.groups[0]
        return self._pagination({
            "master_id": master_id,
            "goods"    : "all",
        })


class Tw6PostExtractor(Tw6Extractor):
    subcategory = "post"
    pattern = BASE_PATTERN + r"/?\?id=(\d+)"
    example = "https://tw6.jp/gallery/?id=12345"

    def posts(self):
        pid = text.parse_int(self.groups[0])
        post = next(self._pagination({
            "last_id": pid,
            "goods"  : "all",
        }), None)
        return (post,) if post and post["gallery_image_id"] == pid else ()


class Tw6SearchExtractor(Tw6Extractor):
    subcategory = "search"
    directory_fmt = ("{category}", "Search", "{search_tags}")
    pattern = BASE_PATTERN + r"/search/?\?([^#]+)"
    example = "https://tw6.jp/gallery/search?word=QUERY"

    def posts(self):
        self.kwdict["search"] = params = text.parse_query(self.groups[0])
        self.kwdict["search_tags"] = params.get("word")
        return self._pagination(params)
