# -*- coding: utf-8 -*-

# Copyright 2016-2025 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://hentaihere.com/"""

from .common import ChapterExtractor, MangaExtractor
from .. import text, util


class HentaihereBase():
    """Base class for hentaihere extractors"""
    category = "hentaihere"
    root = "https://hentaihere.com"


class HentaihereChapterExtractor(HentaihereBase, ChapterExtractor):
    """Extractor for a single manga chapter from hentaihere.com"""
    archive_fmt = "{chapter_id}_{page}"
    pattern = (r"(?:https?://)?(?:www\.)?hentaihere\.com"
               r"(?:/m/S(\d+)/([^/?#]+)|/reader/[^/?#]+/(\d+))")
    example = "https://hentaihere.com/m/S12345/1/1/"

    def __init__(self, match):
        self.manga_id, self.chapter, self.chapter_id = match.groups()
        url = match.string
        if not url.startswith("http"):
            url = "https://" + url
        ChapterExtractor.__init__(self, match, url)

    def metadata(self, page):
        data = util.json_loads(text.extr(
            page, '<script type="application/json" data-reader-data>',
            "</script>") or "null")
        book = (data or {}).get("book") or {}

        ch_num = self.chapter
        if not ch_num:
            ch_num = (book.get("chapter") or "").rsplit(None, 1)[-1]
        chapter, sep, minor = ch_num.partition(".")

        label = text.unescape(text.extr(
            page, 'aria-current="page"', "</a>").rpartition(">")[2])
        title = label.partition(":")[2].strip()

        head = text.unescape(
            (data or {}).get("title") or text.extr(page, "<title>", "</title>"))
        match = text.re(r"Reading (.+) by (.+) Chapter ").match(head)
        if not match:
            match = text.re(
                r"Page 1 \| (.+) \(([^)]+)\) - Chapter \d+: (.+) by "
                r"(.+) at ").match(head)

        mtype = text.extr(page, "/browse/", '"')
        if not mtype:
            m = text.re(
                r"hentaihere\.com/"
                r"(original|doujinshi|artistcg|gamecg|western)/"
            ).search(page)
            mtype = m.group(1) if m else ""

        chapter_id = text.parse_int(
            self.chapter_id or
            text.extr(page, "/download/", '"') or
            text.extr(page, "report/C", '"'))

        if match and match.lastindex == 4:
            manga = match[1]
            author = match[4]
            if not title:
                title = match[3]
            if not mtype:
                mtype = match[2]
        elif match:
            manga = match[1]
            author = match[2]
        else:
            manga = author = ""

        return {
            "manga": book.get("title") or manga,
            "manga_id": text.parse_int(self.manga_id or book.get("id")),
            "chapter": text.parse_int(chapter),
            "chapter_minor": sep + minor,
            "chapter_id": chapter_id,
            "type": mtype.capitalize() if mtype else "",
            "title": title,
            "author": author,
            "lang": "en",
            "language": "English",
        }

    def images(self, page):
        data = text.extr(
            page, '<script type="application/json" data-reader-data>',
            "</script>")
        if data:
            return [
                (url, None)
                for url in util.json_loads(data).get("images") or ()
            ]

        images = text.extr(page, "var rff_imageList = ", ";")
        return [
            ("https://hentaicdn.com/hentai" + part, None)
            for part in util.json_loads(images)
        ]


class HentaihereMangaExtractor(HentaihereBase, MangaExtractor):
    """Extractor for hmanga from hentaihere.com"""
    chapterclass = HentaihereChapterExtractor
    pattern = (r"(?:https?://)?(?:www\.)?hentaihere\.com"
               r"(/m/S\d+|/original/\d+[^/?#]*)/?$")
    example = "https://hentaihere.com/m/S12345"

    def chapters(self, page):
        results = []

        manga = text.unescape(text.extr(page, '"name":"', '"'))
        if not manga:
            title = text.unescape(text.extr(page, "<title>", "</title>"))
            match = text.re(r"Viewing (.+) Hentai by ").match(title)
            manga = match[1] if match else title

        mtype = text.remove_html(text.extr(page, ">Type</dt>", "</dd>")).strip()
        if not mtype:
            mtype = text.extr(page, '<span class="mngType text-danger">[',
                              "]</span>")

        slug = self.page_url.rstrip("/").rpartition("/")[2]
        if slug[:1] == "S":
            slug = slug[1:]
        manga_id = text.parse_int(slug.split("-")[0])

        for opt in text.extract_iter(page, '<option value="', "</option>"):
            chapter_id, _, rest = opt.partition('"')
            url = text.extr(rest, 'data-read="', '"')
            if not url:
                continue
            label = text.unescape(rest.rpartition(">")[2])
            if label.endswith(" (latest)"):
                label = label[:-9]
            chapter, _, title = label.partition(" - ")
            chapter, sep, minor = chapter.split()[-1].partition(".")

            results.append((url, {
                "manga_id": manga_id,
                "manga": manga,
                "chapter": text.parse_int(chapter),
                "chapter_minor": sep + minor,
                "chapter_id": text.parse_int(chapter_id),
                "type": mtype,
                "title": title,
                "lang": "en",
                "language": "English",
            }))

        if results:
            return results

        pos = page.find('itemscope itemtype="http://schema.org/Book') + 1
        manga, pos = text.extract(
            page, '<span itemprop="name">', '</span>', pos)
        mtype, pos = text.extract(
            page, '<span class="mngType text-danger">[', ']</span>', pos)
        manga_id = text.parse_int(
            self.page_url.rstrip("/").rpartition("/")[2][1:])

        while True:
            marker, pos = text.extract(
                page, '<li class="sub-chp clearfix">', '', pos)
            if marker is None:
                return results
            url, pos = text.extract(page, '<a href="', '"', pos)

            chapter, pos = text.extract(page, 'title="Tagged: -">\n', '<', pos)
            chapter_id, pos = text.extract(page, '/C', '"', pos)
            chapter, _, title = text.unescape(chapter).strip().partition(" - ")
            chapter, sep, minor = chapter.partition(".")

            results.append((url, {
                "manga_id": manga_id,
                "manga": manga,
                "chapter": text.parse_int(chapter),
                "chapter_minor": sep + minor,
                "chapter_id": text.parse_int(chapter_id),
                "type": mtype,
                "title": title,
                "lang": "en",
                "language": "English",
            }))
