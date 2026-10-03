# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import senmanga


__tests__ = (
{
    "#url"     : "https://raw.senmanga.com/Bokura-wa-Minna-Kawaisou/37A/1",
    "#category": ("", "senmanga", "chapter"),
    "#class"   : senmanga.SenmangaChapterExtractor,
    "#exception": "NotFoundError",

    "chapter"  : "37A",
    "count"    : 2,
    "extension": "",
    "filename" : r"re:[12]",
    "lang"     : "ja",
    "language" : "Japanese",
    "manga"    : "Bokura wa Minna Kawaisou",
    "page"     : int,
},

{
    "#url"     : "http://raw.senmanga.com/Love-Lab/2016-03/1",
    "#category": ("", "senmanga", "chapter"),
    "#class"   : senmanga.SenmangaChapterExtractor,
    "#exception": "NotFoundError",

    "chapter"  : "2016-03",
    "count"    : 9,
    "extension": "",
    "filename" : r"re:\d",
    "manga"    : "Renai Lab   恋愛ラボ",
},

{
    "#url"     : "https://raw.senmanga.com/akabane-honeko-no-bodyguard/1",
    "#category": ("", "senmanga", "chapter"),
    "#class"   : senmanga.SenmangaChapterExtractor,
    "#exception": "NotFoundError",

    "chapter"  : "1",
    "count"    : 65,
    "extension": "jpg",
    "filename" : r"re:\d+-\w+",
    "manga"    : "Akabane Honeko no Bodyguard",
},

{
    "#url"     : "https://raw.senmanga.com/amama-cinderella/3",
    "#comment" : "no http scheme (); site no longer serves chapters",
    "#category": ("", "senmanga", "chapter"),
    "#class"   : senmanga.SenmangaChapterExtractor,
    "#exception": "NotFoundError",
},

)
