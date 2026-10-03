# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import manganelo


__tests__ = (
{
    "#url"     : "https://www.manganato.gg/manga/danzai-sareta-akuyaku-reijou-wa-gyakkou-shite-kanpeki-na-akujo-wo-mezasu/chapter-4-5",
    "#category": ("manganelo", "manganato", "chapter"),
    "#class"   : manganelo.ManganeloChapterExtractor,
    "#pattern" : r"https://imgs-2.2xstorage.com/danzai-sareta-akuyaku-reijou-wa-gyakkou-shite-kanpeki-na-akujo-wo-mezasu/4\.5/\d+\.webp",
    "#count"   : 24,

    "author"       : "NARAYAMA Bakufu",
    "chapter"      : 4,
    "chapter_id"   : 6,
    "chapter_minor": ".5",
    "count"        : 24,
    "date"         : "type:datetime",
    "date_updated" : "type:datetime",
    "extension"    : "webp",
    "filename"     : str,
    "lang"         : "en",
    "language"     : "English",
    "manga"        : "Danzai sareta Akuyaku Reijou wa, Gyakkou shite Kanpeki na Akujo wo Mezasu",
    "manga_id"     : 32842,
    "page"         : range(1, 24),
},

{
    "#url"     : "https://manganato.gg/manga/aria/chapter-60-2",
    "#category": ("manganelo", "manganato", "chapter"),
    "#class"   : manganelo.ManganeloChapterExtractor,
},

{
    "#url"     : "https://www.manganato.gg/manga/aria",
    "#category": ("manganelo", "manganato", "manga"),
    "#class"   : manganelo.ManganeloMangaExtractor,
    "#pattern" : manganelo.ManganeloChapterExtractor.pattern,
    "#count"   : range(70, 150),

    "author"  : "Amano Kozue",
    "chapter" : range(0, 80),
    "chapter_minor": {"", ".1", ".2", ".5"},
    "date"    : "type:datetime",
    "date_updated": "type:datetime",
    "lang"    : "en",
    "manga"   : "Aria",
    "status"  : "Completed",
    "tags": [
        "Adventure",
        "Comedy",
        "Drama",
        "Sci fi",
        "Shounen",
        "Slice of life",
    ],
},

{
    "#url"     : "https://manganato.gg/manga/aria",
    "#category": ("manganelo", "manganato", "manga"),
    "#class"   : manganelo.ManganeloMangaExtractor,
},

)
