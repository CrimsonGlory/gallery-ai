# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://lensdump.com/"""

from .common import GalleryExtractor, Extractor, Message
from .. import text, util

BASE_PATTERN = r"(?:https?://)?lensdump\.com"


class LensdumpBase():
    """Base class for lensdump extractors"""
    category = "lensdump"
    root = "https://lensdump.com"

    def _init(self):
        self.cookies.set("ld_nsfw_ok", "1", domain="lensdump.com")

    def _pagination(self, page, begin, end):
        seen = set()
        while True:
            yield from text.extract_iter(page, begin, end)

            url = self._next_page_url(page)
            if not url or url in seen:
                return
            seen.add(url)
            page = self.request(url).text

    def _next_page_url(self, page):
        nxt = text.extr(page, ' data-pagination="next"', '>')
        url = text.extr(nxt, 'href="', '"') if nxt else ""
        if not url:
            url = text.extr(page, 'rel="next" href="', '"')
        if not url:
            pos = page.find(" data-load-more ")
            if pos >= 0:
                url = text.rextr(page, 'data-src="', '"', pos)
        if url:
            return text.urljoin(self.root, text.unescape(url))
        return ""


class LensdumpAlbumExtractor(LensdumpBase, GalleryExtractor):
    subcategory = "album"
    pattern = BASE_PATTERN + r"/a/(\w+)(?:/?\?([^#]+))?"
    example = "https://lensdump.com/a/ID"

    def __init__(self, match):
        self.gallery_id, query = match.groups()
        if query:
            url = f"{self.root}/a/{self.gallery_id}/?{query}"
        else:
            url = f"{self.root}/a/{self.gallery_id}"
        GalleryExtractor.__init__(self, match, url)

    def metadata(self, page):
        return {
            "gallery_id": self.gallery_id,
            "title": text.unescape(text.extr(
                page, 'property="og:title" content="', '"').strip())
        }

    def images(self, page):
        seen = set()
        for tile in self._pagination(page, '<a class="tile" ', '>'):
            raw = (text.extr(tile, "data-object='", "'") or
                   text.extr(tile, 'data-object="', '"'))
            if not raw:
                continue
            try:
                data = util.json_loads(text.unquote(raw))
            except Exception:
                continue

            image = data.get("image")
            if image.__class__ is dict:
                image_url = image.get("url") or data.get("url")
            else:
                image_url = data.get("url")
                image = {}
            if not image_url or image_url.endswith("/404.png"):
                continue

            name = data.get("filename") or ""
            image_id = data.get("name")
            if not image_id:
                path = data.get("path_viewer") or ""
                image_id = path.rpartition("/")[2]
            if not image_id:
                image_id = name[:name.rfind(".")] if "." in name else name
            if not image_id or image_id in seen:
                continue
            seen.add(image_id)

            user = data.get("user")
            image_title = data.get("title")
            if image_title is not None:
                image_title = text.unescape(image_title)

            yield (image_url, {
                "id"       : image_id,
                "url"      : image_url,
                "title"    : image_title,
                "name"     : data.get("filename"),
                "filename" : image_id,
                "extension": data.get("extension"),
                "width"    : text.parse_int(data.get("width")),
                "height"   : text.parse_int(data.get("height")),
                "size"     : text.parse_int(image.get("size")),
                "user"     : user.get("username") if user else "",
            })


class LensdumpAlbumsExtractor(LensdumpBase, Extractor):
    """Extractor for album list from lensdump.com"""
    subcategory = "albums"
    pattern = BASE_PATTERN + r"/(?![ai]/)([^/?#]+)(?:/?\?([^#]+))?"
    example = "https://lensdump.com/USER"

    def items(self):
        user, query = self.groups
        url = f"{self.root}/{user}/"
        if query:
            params = text.parse_query(query)
        else:
            params = {"sort": "date_asc", "page": "1"}
        page = self.request(url, params=params).text

        data = {"_extractor": LensdumpAlbumExtractor}
        seen = set()
        pages_seen = set()
        while True:
            paths = list(text.extract_iter(page, 'data-url-short="', '"'))
            if not paths:
                paths = [
                    "/a/" + code
                    for code in text.extract_iter(page, 'data-code="', '"')
                ]
            for album_path in paths:
                album_url = text.urljoin(self.root, album_path)
                if album_url in seen:
                    continue
                seen.add(album_url)
                yield Message.Queue, album_url, data

            next_url = self._next_page_url(page)
            if not next_url or next_url in pages_seen:
                return
            pages_seen.add(next_url)
            page = self.request(next_url).text


class LensdumpImageExtractor(LensdumpBase, Extractor):
    """Extractor for individual images on lensdump.com"""
    subcategory = "image"
    filename_fmt = "{category}_{id}{title:?_//}.{extension}"
    directory_fmt = ("{category}",)
    archive_fmt = "{id}"
    pattern = (r"(?:https?://)?(?:(?:i\d?\.)?lensdump\.com|\w\.l3n\.co)"
               r"/(?:i/)?(\w+)")
    example = "https://lensdump.com/i/ID"

    def items(self):
        key = self.groups[0]
        page = self.request(f"{self.root}/i/{key}").text

        cfg = text.extr(page, "window.lensConfig = ", ";")
        try:
            file = (util.json_loads(cfg) if cfg else {}).get("file") or {}
        except Exception:
            file = {}

        url = file.get("url") or text.extr(
            page, 'property="og:image" content="', '"')
        if not url:
            url = self._direct_url(key, page)

        date_str = (
            text.extr(page, 'ld-iv-chip" title="', '"') or
            text.extr(page, '<dt>Uploaded</dt><dd title="', '"') or
            text.extr(page, 'datetime="', '"')
        ).replace(" UTC", "")

        data = {
            "id"    : key,
            "title" : text.unescape(text.extr(
                page, 'property="og:title" content="', '"')),
            "url"   : url,
            "width" : text.parse_int(
                file.get("width") or
                text.extr(page, 'property="og:image:width" content="', '"') or
                text.extr(page, 'property="image:width" content="', '"')),
            "height": text.parse_int(
                file.get("height") or
                text.extr(page, 'property="og:image:height" content="', '"') or
                text.extr(page, 'property="image:height" content="', '"')),
            "date"  : self.parse_datetime_iso(date_str),
        }

        text.nameext_from_url(url, data)
        yield Message.Directory, "", data
        yield Message.Url, url, data

    def _direct_url(self, key, page):
        src = self.url
        if ".l3n.co/" in src:
            return src.replace("/i/", "/", 1)

        ext = text.extr(
            page, "<dt>Type and size</dt><dd>", " ").strip().lower()
        if ext == "jpeg":
            ext = "jpg"
        if not ext:
            return ""

        for host in "abcd":
            cand = f"https://{host}.l3n.co/{key}.{ext}"
            resp = self.request(cand, method="HEAD", fatal=False)
            if resp.status_code < 400:
                return cand
        return ""
