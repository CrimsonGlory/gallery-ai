# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://mangayi.com/"""

from .common import ChapterExtractor, MangaExtractor
from .. import text, util

BASE_PATTERN = r"(?:https?://)?(?:www\.)?mangayi\.com"


class MangayiBase():
    """Base class for mangayi.com extractors"""
    category = "mangayi"
    root = "https://mangayi.com"


class MangayiChapterExtractor(MangayiBase, ChapterExtractor):
    """Extractor for manga-chapters from mangayi.com"""
    pattern = BASE_PATTERN + r"(/read/[^/?#]+/(?:v(\d+)/)?chapter/\d+[^/?#]*)"
    example = "https://mangayi.com/read/TITLE/chapter/1/"

    def metadata(self, page):
        data = self._jsonld(page, "ComicIssue")
        if not data:
            data = util.json_loads("{" + text.extr(
                page, '","@type":"ComicIssue",', '</script>'))
        chapter, dot, minor = data["issueNumber"].partition(".")

        return {
            "manga"        : data["isPartOf"]["name"],
            "title"        : data["name"].partition(":")[2].strip(),
            "volume"       : text.parse_int(self.groups[1]),
            "chapter"      : text.parse_int(chapter),
            "chapter_minor": dot + minor,
            "date"         : self.parse_datetime_iso(data["datePublished"]),
            "lang"         : data["inLanguage"],
        }

    def images(self, page):
        images = []
        seen = set()
        for chunk in text.extract_iter(page, '<img class="l', ">"):
            url = text.extr(chunk, 'src="', '"')
            if not url:
                continue
            url = text.ensure_http_scheme(url)
            if url in seen:
                continue
            seen.add(url)
            images.append((url, None))
        if images:
            return images

        data = util.json_loads("{" + text.extr(
            page, '","@type":"MediaGallery",', '</script>'))
        return [
            (text.ensure_http_scheme(image["url"]), None)
            for image in data["associatedMedia"]
        ]

    def _jsonld(self, page, type):
        for raw in text.extract_iter(
                page, 'type="application/ld+json">', "</script>"):
            try:
                data = util.json_loads(raw)
            except Exception:
                continue
            if data.get("@type") == type:
                return data
        return None


class MangayiMangaExtractor(MangayiBase, MangaExtractor):
    chapterclass = MangayiChapterExtractor
    pattern = BASE_PATTERN + r"(/read/[^/?#]+)"
    example = "https://mangayi.com/read/TITLE/"

    def chapters(self, page):
        manga = util.json_loads("{" + text.extr(
            page, '","@type":"ComicSeries",', '</script>'))["name"]

        results = []
        seen = set()
        for chunk in text.extract_iter(page, 'class="c" href="', "</a>"):
            path, _, rest = chunk.partition('"')
            if "/chapter/" not in path or path in seen:
                continue
            seen.add(path)
            url = text.urljoin(self.root, path)
            chapter = url[url.rfind("/", 0, -2)+1:-1]
            chapter, sep, minor = chapter.partition("-")
            title = text.unescape(
                text.extr(rest, 'class="t"', "</p>").rpartition(">")[2])

            results.append((url, {
                "manga"        : manga,
                "chapter"      : text.parse_int(chapter),
                "chapter_minor": sep + minor,
                "title"        : title.partition(":")[-1].strip(),
                "lang"         : "en",
            }))

        if results:
            return results

        data = util.json_loads("{" + text.extr(
            page, '","@type":"ItemList",', '</script>'))
        for ch in data["itemListElement"]:
            url = ch["url"]
            chapter = url[url.rfind("/", 0, -2)+1:-1]
            chapter, sep, minor = chapter.partition("-")

            results.append((url, {
                "manga"        : manga,
                "chapter"      : text.parse_int(chapter),
                "chapter_minor": sep + minor,
                "title"        : ch["name"].partition(":")[2].strip(),
                "lang"         : "en",
            }))
        return results
