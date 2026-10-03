# -*- coding: utf-8 -*-

# Copyright 2025-2026 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://imhentai.xxx/ and mirror sites"""

from urllib.parse import urlencode

from .common import GalleryExtractor, BaseExtractor, Message
from .. import text, util


class ImhentaiExtractor(BaseExtractor):
    basecategory = "IMHentai"

    def _pagination(self, url):
        prev = None
        seen_urls = set()
        base = self.root + "/gallery/"
        data = {"_extractor": ImhentaiGalleryExtractor}

        while url not in seen_urls:
            seen_urls.add(url)
            page_full = self.request(url).text
            page = page_full
            pos = page.find('class="ranking_list"')
            if pos >= 0:
                page = page[:pos]

            extr = text.extract_from(page)
            found = 0

            while True:
                gallery_id = extr('href="/gallery/', '"')
                if gallery_id == prev:
                    continue
                if not gallery_id:
                    break
                yield Message.Queue, base + gallery_id, data
                prev = gallery_id
                found += 1

            href = text.rextr(page_full, "class='page-link' href='", "'")
            if not href or href == "#":
                pos = page_full.find('rel="next"')
                href = (text.rextr(page_full, 'href="', '"', pos)
                        if pos >= 0 else None)
            if not found or not href or href == "#":
                return
            url = self._join_next(url, href)

    def _join_next(self, current, href):
        if href[0] == "/":
            href = ("https:" + href) if href.startswith("//") else (
                self.root + href)
        elif href[0] == "?":
            href = current.partition("?")[0] + href

        cur_q = text.parse_query(current.partition("?")[2])
        nxt_q = text.parse_query(href.partition("?")[2])
        if cur_q and nxt_q and set(nxt_q) <= {"page"}:
            cur_q.update(nxt_q)
            href = href.partition("?")[0] + "?" + urlencode(cur_q)
        return href


BASE_PATTERN = ImhentaiExtractor.update({
    "imhentai": {
        "root": "https://imhentai.xxx",
        "pattern": r"(?:www\.)?imhentai\.xxx",
    },
    "hentaiera": {
        "root": "https://hentaiera.com",
        "pattern": r"(?:www\.)?hentaiera\.com",
    },
    "hentairox": {
        "root": "https://hentairox.com",
        "pattern": r"(?:www\.)?hentairox\.com",
    },
    "hentaifox": {
        "root": "https://hentaifox.com",
        "pattern": r"(?:www\.)?hentaifox\.com",
    },
    "hentaienvy": {
        "root": "https://hentaienvy.com",
        "pattern": r"(?:www\.)?hentaienvy\.com",
    },
    "hentaizap": {
        "root": "https://hentaizap.com",
        "pattern": r"(?:www\.)?hentaizap\.com",
    },
})


class ImhentaiGalleryExtractor(ImhentaiExtractor, GalleryExtractor):
    """Extractor for imhentai galleries"""
    pattern = BASE_PATTERN + r"/(?:gallery|view)/(\d+)"
    example = "https://imhentai.xxx/gallery/12345/"

    def __init__(self, match):
        ImhentaiExtractor.__init__(self, match)
        self.gallery_id = self.groups[-1]
        self.page_url = f"{self.root}/gallery/{self.gallery_id}/"

    def metadata(self, page):
        if ("hnv-gallery-metadata" in page or
                "hz-gallery-metadata" in page or
                'id="gallery-title"' in page or
                "hnv-gallery-entity" in page or
                "hz-gallery-entity" in page):
            return self._metadata_hnv(page)

        extr = text.extract_from(page)
        title = extr("<h1>", "<")
        title_alt = extr('class="subtitle">', "<")
        end = "</li>" if extr('<ul class="galleries_info', ">") else "</ul>"

        data = {
            "gallery_id": text.parse_int(self.gallery_id),
            "title"     : text.unescape(title),
            "title_alt" : text.unescape(title_alt),
            "parody"    : self._split(extr(">Parodies", end)),
            "character" : self._split(extr(">Characters", end)),
            "tags"      : self._split(extr(">Tags", end)),
            "artist"    : self._split(extr(">Artists", end)),
            "group"     : self._split(extr(">Groups", end)),
            "language"  : self._split(extr(">Languages", end)),
            "type"      : extr("href='/category/", "/"),
        }

        if data["language"]:
            data["lang"] = util.language_to_code(data["language"][0])

        return data

    def _metadata_hnv(self, page):
        def group(label):
            start = page.find(f">{label}:</span>")
            if start < 0:
                start = page.find(f">{label}</span>")
            if start < 0:
                return []
            end = page.find("-gallery-entity-group", start + 1)
            for marker in ("-gallery-pages", "-gallery-actions",
                           "-gallery-votes"):
                pos = page.find(marker, start + 1)
                if pos > start and (end < 0 or pos < end):
                    end = pos
            html = page[start:end if end > start else start + 4000]
            names = [
                text.unescape(name)
                for name in text.extract_iter(html, 'title="', '"')
                if name
            ]
            if not names:
                names = []
                for match in text.re(
                    r'gallery-tag__name">([^<]+)'
                    r'(?:<span[^>]*>\s*([^<]*)</span>)?'
                ).finditer(html):
                    name = " ".join(
                        (match.group(1) + (match.group(2) or "")).split())
                    if "|" in name:
                        name = " | ".join(
                            part.strip() for part in name.split("|")
                            if part.strip())
                    if name:
                        names.append(text.unescape(name))
            names.sort()
            return names

        title = text.unescape(text.extr(
            page, 'id="gallery-title">', "<") or text.extr(page, "<h1>", "<"))
        title_alt = text.unescape(
            text.extr(page, 'hnv-gallery-description">', "<") or
            text.extr(page, 'hz-gallery-description">', "<"))
        data = {
            "gallery_id": text.parse_int(self.gallery_id),
            "title"     : title,
            "title_alt" : title_alt,
            "parody"    : group("Parodies"),
            "character" : group("Characters"),
            "tags"      : group("Tags"),
            "artist"    : group("Artists"),
            "group"     : group("Groups"),
            "language"  : group("Languages"),
            "type"      : (group("Category") or [""])[0],
        }
        if data["language"]:
            data["lang"] = util.language_to_code(data["language"][0])
        return data

    def _split(self, html):
        results = []
        for tag in text.extract_iter(html, ">", "</a>"):
            badge = ("badge'>" in tag or "class='badge" in tag)
            tag = text.remove_html(tag)
            if badge:
                tag = tag.rpartition(" ")[0]
            results.append(tag)
        results.sort()
        return results

    def images(self, page):
        base = text.extr(page, 'data-src="', '"').rpartition("/")[0] + "/"
        exts = {"j": "jpg", "p": "png", "g": "gif", "w": "webp", "a": "avif"}

        try:
            data = util.json_loads(text.extr(page, "$.parseJSON('", "'"))
        except Exception:
            data = None

        if data is None and (
                "hnv-gallery-thumb" in page or
                "hz-gallery-thumb" in page or
                "data-total-pages" in page):
            return self._images_hnv(page)

        if data is None:
            self.log.warning("%s: Missing image data", self.gallery_id)

            def _fallback_exts(i):
                for ext in util.advance(exts.values(), 1):
                    yield f"{base}{i}.{ext}"
            cnt = text.parse_int(text.extr(
                page, 'id="load_pages" value="', '"'))
            return [(f"{base}{i}.jpg", {"_fallback": _fallback_exts(i)})
                    for i in range(1, cnt+1)]

        results = []
        for i in map(str, range(1, len(data)+1)):
            ext, width, height = data[i].split(",")
            url = f"{base}{i}.{exts[ext]}"
            results.append((url, {
                "width" : text.parse_int(width),
                "height": text.parse_int(height),
            }))
        return results

    def _images_hnv(self, page):
        cnt = text.parse_int(text.extr(page, 'data-total-pages="', '"'))
        match = text.re(
            r'(https://m\d+\.[^"\s]+/\d+/[^"/\s]+/)'
            r'(?:\d+t|cover)\.(\w+)').search(page)
        if not match:
            src = text.extr(page, "gallery-thumb__image", "</span>")
            url = text.extr(src, 'src="', '"')
            if not url:
                return ()
            ext = url.rsplit(".", 1)[-1]
            base = url.rsplit("/", 1)[0] + "/"
        else:
            base, ext = match.group(1), match.group(2)
        if cnt < 1:
            pages_html = text.extr(page, "gallery-pages", "</div>")
            cnt = text.parse_int(
                text.remove_html(pages_html).rpartition(":")[-1])
        if cnt < 1:
            cnt = sum(1 for _ in text.extract_iter(
                page, "gallery-thumb", "</div>"))
        return [(f"{base}{i}.{ext}", None) for i in range(1, cnt + 1)]


class ImhentaiTagExtractor(ImhentaiExtractor):
    """Extractor for imhentai tag searches"""
    subcategory = "tag"
    pattern = (BASE_PATTERN + r"(/(?:"
               r"artist|category|character|group|language|parody|tag"
               r")/([^/?#]+))")
    example = "https://imhentai.xxx/tag/TAG/"

    def items(self):
        url = self.root + self.groups[-2] + "/"
        return self._pagination(url)


class ImhentaiSearchExtractor(ImhentaiExtractor):
    """Extractor for imhentai search results"""
    subcategory = "search"
    pattern = BASE_PATTERN + r"(/(?:advanced-)?search/?\?[^#]+|/[^/?#]+/?)"
    example = "https://imhentai.xxx/search/?key=QUERY"

    def items(self):
        return self._pagination(self.root + self.groups[-1])
