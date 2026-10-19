# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import hentaihere


__tests__ = (
{
    "#url"     : "https://hentaihere.com/m/S13812/1/1/",
    "#category": ("", "hentaihere", "chapter"),
    "#class"   : hentaihere.HentaihereChapterExtractor,
    "#pattern" : r"https://hermes\.hentai\.direct/hentai/13812/1/hcdn00\d+\.jpg",
    "#count"   : 16,

    "author"       : "Morris",
    "chapter"      : 1,
    "chapter_id"   : 20902,
    "chapter_minor": "",
    "count"        : 16,
    "lang"         : "en",
    "language"     : "English",
    "manga"        : "Amazon Elixir",
    "manga_id"     : 13812,
    "page"         : int,
    "title"        : "Amazon Elixir [Oneshot]",
    "type"         : "Original",
},

{
    "#url"     : "https://hentaihere.com/m/S23048/1.5/1/",
    "#category": ("", "hentaihere", "chapter"),
    "#class"   : hentaihere.HentaihereChapterExtractor,
    "#pattern" : r"https://hermes\.hentai\.direct/hentai/23048/1\.5/ccdn00\d+\.jpg",
    "#count"   : 32,

    "author"       : "Shinozuka Yuuji",
    "chapter"      : 1,
    "chapter_id"   : 80186,
    "chapter_minor": ".5",
    "count"        : 32,
    "lang"         : "en",
    "language"     : "English",
    "manga"        : "High School Slut's Love Consultation",
    "manga_id"     : 23048,
    "page"         : int,
    "title"        : "High School Slut's Love Consultation + Girlfriend [Full Color]",
    "type"         : "Original",
},

{
    "#url"     : "https://hentaihere.com/m/S13812",
    "#category": ("", "hentaihere", "manga"),
    "#class"   : hentaihere.HentaihereMangaExtractor,
    "#pattern"      : r"https://hentaihere\.com/reader/13812-amazon-elixir/\d+/page-1",
    "#count"        : ">= 1",
},

{
    "#url"     : "https://hentaihere.com/m/S7608",
    "#category": ("", "hentaihere", "manga"),
    "#class"   : hentaihere.HentaihereMangaExtractor,
    "#pattern" : r"https://hentaihere\.com/reader/7608-oshikake-riot/\d+/page-1",
    "#count"   : 10,

    "chapter"      : int,
    "chapter_id"   : int,
    "chapter_minor": "",
    "lang"         : "en",
    "language"     : "English",
    "manga"        : "Oshikake Riot",
    "manga_id"     : 7608,
    "title"        : r"re:Oshikake Riot( \d+)?",
    "type"         : "Original",
},

)
