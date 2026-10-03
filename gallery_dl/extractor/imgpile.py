# -*- coding: utf-8 -*-

# Copyright 2025 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://imgpile.com/"""

from .common import Extractor, Message
from .. import text

BASE_PATTERN = r"(?:https?://)?(?:www\.)?imgpile\.com"


class ImgpileExtractor(Extractor):
    """Base class for imgpile extractors"""
    category = "imgpile"
    root = "https://imgpile.com"
    directory_fmt = ("{category}", "{post[author]}",
                     "{post[title]} ({post[id_slug]})")
    archive_fmt = "{post[id_slug]}_{id}"


class ImgpilePostExtractor(ImgpileExtractor):
    subcategory = "post"
    pattern = BASE_PATTERN + r"/p/(\w+)"
    example = "https://imgpile.com/p/AbCdEfG"

    def items(self):
        post_id = self.groups[0]
        url = f"{self.root}/p/{post_id}"
        page = self.request(url).text

        title = text.unescape(text.extr(page, "<title>", " - imgpile<"))
        author = text.extr(
            page, '"author":{"@type":"Person","name":"', '"')
        post_num = text.parse_int(text.extr(page, '"id",', ","))
        score = text.parse_int(text.extr(page, '"score",', ","))
        views = text.parse_int(text.extr(page, '"viewCount",', ","))
        tags = text.re(r'"name","([^"]+)","').findall(
            text.extr(page, '"name","', '"username"'))
        if not tags:
            tags = text.split_html(text.extr(
                page, " <!-- Tags -->", '<!-- "'))

        post = {
            "id_slug": post_id,
            "title"  : title,
            "id"     : post_num,
            "author" : author,
            "score"  : score,
            "views"  : views,
            "tags"   : tags,
        }

        files = self._extract_files(page)
        data = {"post": post}
        data["count"] = post["count"] = len(files)

        yield Message.Directory, "", data
        for data["num"], file in enumerate(files, 1):
            data.update(file)
            url = file["url"]
            yield Message.Url, url, text.nameext_from_url(url, data)

    def _extract_files(self, page):
        files = []
        seen = set()
        media_re = text.re(
            r"cdn\.imgpile\.com/f/([A-Za-z0-9]+)"
            r"(?:_wm)?(?:_(?:xs|sm|md|lg|xl))?"
            r"(\.(?:jpe?g|png|gif|webp|mp4))")
        for slug, ext in media_re.findall(page):
            if slug in seen:
                continue
            seen.add(slug)
            files.append({
                "id_slug": slug,
                "id"     : len(seen),
                "url"    : f"https://cdn.imgpile.com/f/{slug}{ext}",
            })
        if files:
            return files

        extr = text.extract_from(page)
        while True:
            media = extr('class="post-media', '</div>')
            if not media:
                break
            href = (text.extr(media, '<a href="', '"') or
                    "http" + text.extr(media, '<a href="http', '"'))
            if href.startswith("//"):
                href = "https:" + href
            files.append({
                "id_slug": text.extr(media, 'data-id="', '"'),
                "id" : text.parse_int(text.extr(
                    media, 'data-media-id="', '"')),
                "url": href,
            })
        return files


class ImgpileUserExtractor(ImgpileExtractor):
    subcategory = "user"
    pattern = BASE_PATTERN + r"/u/([^/?#]+)"
    example = "https://imgpile.com/u/USER"

    def items(self):
        user = self.groups[0]
        page = self.request(f"{self.root}/u/{user}").text
        slugs = list(dict.fromkeys(
            text.re(r'href="(?:https://imgpile\.com)?/p/(\w+)"').findall(page)
        ))
        if not slugs:
            url = self.root + "/api/v1/posts"
            params = {
                "limit"     : "100",
                "sort"      : "latest",
                "period"    : "all",
                "visibility": "public",
                "username"  : user,
            }
            headers = {
                "Accept"      : "application/json",
                "Content-Type": "application/json",
            }
            data = self.request_json(url, params=params, headers=headers)
            self.kwdict["total"] = data.get("meta", {}).get("total")
            slugs = [item["slug"] for item in data.get("data") or ()]

        base = self.root + "/p/"
        data = {"_extractor": ImgpilePostExtractor}
        for slug in slugs:
            yield Message.Queue, base + slug, data
