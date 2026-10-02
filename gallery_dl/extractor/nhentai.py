# -*- coding: utf-8 -*-

# Copyright 2015-2026 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://nhentai.net/"""

import collections
import random
from urllib.parse import quote, unquote
from .common import GalleryExtractor, Extractor, Message
from .. import text, util


class NhentaiGalleryExtractor(GalleryExtractor):
    """Extractor for image galleries from nhentai.net"""
    category = "nhentai"
    root = "https://nhentai.net"
    pattern = r"(?:https?://)?nhentai\.net/g/(\d+)"
    example = "https://nhentai.net/g/12345/"

    def _init(self):
        self.headers_api = {}
        if api_key := self.config("api-key"):
            self.headers_api["Authorization"] = "Key " + api_key

    def metadata(self, _):
        url = f"{self.root}/api/v2/galleries/{self.groups[0]}"
        self.data = data = self.request_json(
            url, headers=self.headers_api)

        title = data["title"]
        title_en = title.get("english", "")
        title_ja = title.get("japanese", "")

        info = collections.defaultdict(list)
        for tag in data["tags"]:
            info[tag["type"]].append(tag["name"])

        language = ""
        for language in info["language"]:
            if language != "translated":
                language = language.capitalize()
                break

        return {
            "title"     : title_en or title_ja,
            "title_en"  : title_en,
            "title_ja"  : title_ja,
            "title_pretty": title.get("pretty", ""),
            "gallery_id": data["id"],
            "media_id"  : text.parse_int(data["media_id"]),
            "date"      : self.parse_timestamp(data["upload_date"]),
            "scanlator" : info.get("scanlator", ""),
            "artist"    : info["artist"],
            "group"     : info["group"],
            "parody"    : info["parody"],
            "characters": info["character"],
            "tags"      : info["tag"],
            "type"      : info["category"][0] if "category" in info else "",
            "lang"      : util.language_to_code(language),
            "language"  : language,
        }

    def images(self, _):
        data = self.data
        return [
            (f"https://i{random.randint(1, 4)}.nhentai.net/{page['path']}", {
                "width" : page["width"],
                "height": page["height"],
            })
            for page in data["pages"]
        ]


class NhentaiExtractor(Extractor):
    """Base class for nhentai extractors"""
    category = "nhentai"
    root = "https://nhentai.net"

    def _init(self):
        self.headers_api = {}
        if api_key := self.config("api-key"):
            self.headers_api["Authorization"] = "Key " + api_key

    def __init__(self, match):
        Extractor.__init__(self, match)
        self.path, self.query = match.groups()

    def items(self):
        data = {"_extractor": NhentaiGalleryExtractor}
        for gallery_id in self.galleries():
            url = f"{self.root}/g/{gallery_id}/"
            data["gallery_id"] = text.parse_int(gallery_id)
            yield Message.Queue, url, data

    def request_api(self, endpoint, params=None):
        url = f"{self.root}/api/v2/{endpoint}"
        return self.request_json(url, params=params, headers=self.headers_api)

    def _pagination(self, endpoint, params):
        params.setdefault("page", 1)

        while True:
            data = self.request_api(endpoint, params)
            yield from (item["id"] for item in data["result"])

            if params["page"] >= data["num_pages"]:
                return
            params["page"] += 1


class NhentaiTagExtractor(NhentaiExtractor):
    """Extractor for nhentai tag searches"""
    subcategory = "tag"
    pattern = (r"(?:https?://)?nhentai\.net("
               r"/(?:artist|category|character|group|language|parody|tag)"
               r"/[^/?#]+(?:/popular[^/?#]*)?/?)(?:\?([^#]+))?")
    example = "https://nhentai.net/tag/TAG/"

    def galleries(self):
        tag_type, slug, *sort_path = self.path.strip("/").split("/")
        tag = self.request_api(
            f"tags/{quote(tag_type, safe='')}/"
            f"{quote(unquote(slug), safe='')}")

        params = text.parse_query(self.query)
        api_params = {
            "tag_id": tag["id"],
            "page": text.parse_int(params.get("page"), 1),
        }
        if sort := params.get("sort") or (sort_path[0] if sort_path else None):
            api_params["sort"] = sort

        return self._pagination("galleries/tagged", api_params)


class NhentaiSearchExtractor(NhentaiExtractor):
    """Extractor for nhentai search results"""
    subcategory = "search"
    pattern = r"(?:https?://)?nhentai\.net(/search/?)\?([^#]+)"
    example = "https://nhentai.net/search/?q=QUERY"

    def galleries(self):
        params = text.parse_query(self.query)
        api_params = {
            "query": params.get("q", ""),
            "page": text.parse_int(params.get("page"), 1),
        }
        if sort := params.get("sort"):
            api_params["sort"] = sort

        return self._pagination("search", api_params)


class NhentaiFavoriteExtractor(NhentaiExtractor):
    """Extractor for nhentai favorites"""
    subcategory = "favorite"
    pattern = r"(?:https?://)?nhentai\.net(/favorites/?)(?:\?([^#]+))?"
    example = "https://nhentai.net/favorites/"

    def galleries(self):
        params = text.parse_query(self.query)
        api_params = {
            "page": text.parse_int(params.get("page"), 1),
        }
        if query := params.get("q"):
            api_params["q"] = query

        return self._pagination("favorites", api_params)
