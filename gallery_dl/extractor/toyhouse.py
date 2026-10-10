# -*- coding: utf-8 -*-

# Copyright 2022-2026 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://toyhou.se/"""

from .common import Extractor, Message
from .. import text, util

BASE_PATTERN = r"(?:https?://)?(?:www\.)?toyhou\.se"


class ToyhouseExtractor(Extractor):
    """Base class for toyhouse extractors"""
    category = "toyhouse"
    root = "https://toyhou.se"
    directory_fmt = ("{category}", "{user|artists!S}")
    archive_fmt = "{id}"

    def _init(self):
        self.offset = 0

    def items(self):
        for post in util.advance(self.posts(), self.offset):
            text.nameext_from_url(post["url"], post)
            post["id"], _, post["hash"] = post["filename"].partition("_")
            yield Message.Directory, "", post
            yield Message.Url, post["url"], post

    def skip_files(self, num):
        self.offset += num
        return num

    def _parse_post(self, post, needle=' href="'):
        extr = text.extract_from(post)
        data = {
            "url": extr(needle, '"'),
            "detail": "\n".join(text.split_html(extr(
                'class="image-detail', 'class="image-credit'))[2:-2]),
            "date": (v := extr('', "</div")) and
            self.parse_datetime(
                v[v.find('mb-1">')+6:], "%d %b %Y, %I:%M:%S %p"),
            "artists": text.split_html(extr(
                '<div class="artist-credit',
                '<div class="image-character'))[1:],
            "characters": text.split_html(
                extr('', 'class="image-') or
                extr('', 'id="footer"'))[2:-1],
        }

        url = data["url"]
        if "/watermarks/" in url:
            data["status"] = "watermark"
        elif "/thumbnails/" in url:
            data["status"] = "thumbnail"
        else:
            data["status"] = "original"

        return data

    def _pagination(self, url):
        params = {"page": 1}

        while True:
            page = self.request(url, params=params).text

            if params["page"] == 1:
                if ">Content Warning<" in page and \
                        self._accept_content_warning(page):
                    continue
                self._extract_webpage(page)

            cnt = 0
            for post in text.extract_iter(
                    page, '<li class="gallery-item">', '</li>'):
                cnt += 1
                yield self._parse_post(post)

            if cnt < 18:
                break
            params["page"] += 1

    def _accept_content_warning(self, page):
        data = {
            text.extr(input, 'name="', '"'): text.unescape(
                text.extr(input, 'value="', '"'))
            for input in text.extract_iter(page, "<input ", ">")
        }

        if not data.get("_token"):
            return False
        self.log.info("Accepting 'Content Warning'")
        self.request(self.root + "/~account/warnings/accept",
                     method="POST", data=data, allow_redirects=False)
        return True


class ToyhouseArtExtractor(ToyhouseExtractor):
    """Extractor for artworks of a toyhouse user"""
    subcategory = "art"
    pattern = BASE_PATTERN + r"/([^/?#]+)/art"
    example = "https://www.toyhou.se/USER/art"

    def posts(self):
        return self._pagination(f"{self.root}/{self.groups[0]}/art")

    def _extract_webpage(self, page):
        if user := text.extr(page, 'class="display-user', '</'):
            kw = self.kwdict
            kw["user"] = text.extr(user, 'href="https://toyhou.se/', '"')
            kw["display_name"] = text.unescape(user[user.rfind(">")+1:])


class ToyhouseCharacterGalleryExtractor(ToyhouseExtractor):
    """Extractor for a toyhouse character's gallery"""
    subcategory = "character-gallery"
    directory_fmt = ("{category}", "{user}", "Characters",
                     "{character} ({character_id})",
                     "{tab:?//}{tab_id:? (/)/}")
    pattern = BASE_PATTERN + r"/(\d+\.[\w-]*)/(?:(\d+\.[\w-]*)/)?gallery"
    example = "https://www.toyhou.se/12345.CHARACTER/gallery"

    def posts(self):
        char, tab = self.groups
        if tab is None:
            url = f"{self.root}/{char}/gallery"
        else:
            cid, _, cname = char.partition(".")
            url = f"{self.root}/{cid}.{cname or 'name'}/{tab}/gallery"
        return self._pagination(url)

    def _extract_webpage(self, page):
        extr = text.extract_from(page)
        kw = self.kwdict
        if user := extr('class="user-name">', '</'):
            kw["user"] = text.extr(user, 'href="https://toyhou.se/', '"')
            kw["display_name"] = text.unescape(user[user.rfind(">")+1:])
        if folder := extr('class="character-folder', '</a'):
            kw["folder"] = text.unescape(folder[folder.rfind(">")+1:])
            kw["folder_id"] = text.extr(folder, '/folder:', '"')
        if char := extr('class="character-name">', '</'):
            kw["character"] = text.unescape(char[char.rfind(">")+1:])
            kw["character_id"], _, kw["character_slug"] = text.extr(
                char, ' href="/', '"').partition(".")
        if tab := self.groups[1]:
            kw["tab_id"] = tid = tab.partition(".")[0]
            kw["tab_slug"] = extr(f"/{tid}.", '"')
            kw["tab"] = text.unescape(extr("</i>", "<").strip())


class ToyhouseImageExtractor(ToyhouseExtractor):
    """Extractor for individual toyhouse images"""
    subcategory = "image"
    pattern = (r"(?:https?://)?(?:"
               r"(?:www\.)?toyhou\.se/(~images|\d+\.\w+)|"
               r"f\d+\.toyhou\.se/file/[^/?#]+/(?:image|watermark|thumbnail)s"
               r")/(\d+)")
    example = "https://toyhou.se/~images/12345"

    def posts(self):
        path, image_id = self.groups
        if path is None:
            path = "~images"
        url = f"{self.root}/{path}/{image_id}"
        page = self.request(url).text
        if ">Content Warning<" in page and self._accept_content_warning(page):
            page = self.request(url).text
        return (self._parse_post(page, '<img class="mw-100" src="'),)
