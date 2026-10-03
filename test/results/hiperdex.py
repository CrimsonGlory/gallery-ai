# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import hiperdex
from gallery_dl import exception


__tests__ = (
{
    "#url"     : "https://hiperdex.com/manga/the-second-coming-of-gluttony/1/",
    "#category": ("", "hiperdex", "chapter"),
    "#class"   : hiperdex.HiperdexChapterExtractor,
    "#pattern" : r"https://i\d+\.r2d2storage\.com/data/manga_\w+/[0-9a-f]+/\w+\.webp",
    "#count"   : 37,

    "artist"       : list,
    "author"       : list,
    "chapter"      : 1,
    "chapter_minor": "",
    "description"  : str,
    "manga"        : "The Second Coming of Gluttony",
    "score"        : {int, float},
    "type"         : "manhwa",
    "year"         : 2019,
},

{
    "#url"     : "https://hiperdex.com/mangas/domestic-na-kanojo/154-5/",
    "#category": ("", "hiperdex", "chapter"),
    "#class"   : hiperdex.HiperdexChapterExtractor,
    "#exception": exception.HttpError,
},

{
    "#url"     : "https://1sthiperdex.com/manga/domestic-na-kanojo/154-5/",
    "#category": ("", "hiperdex", "chapter"),
    "#class"   : hiperdex.HiperdexChapterExtractor,
    "#exception": exception.HttpError,
},

{
    "#url"     : "https://hiperdex2.com/manga/domestic-na-kanojo/154-5/",
    "#category": ("", "hiperdex", "chapter"),
    "#class"   : hiperdex.HiperdexChapterExtractor,
    "#exception": exception.HttpError,
},

{
    "#url"     : "https://hiperdex.net/manga/domestic-na-kanojo/154-5/",
    "#category": ("", "hiperdex", "chapter"),
    "#class"   : hiperdex.HiperdexChapterExtractor,
    "#exception": exception.HttpError,
},

{
    "#url"     : "https://hiperdex.info/manga/domestic-na-kanojo/154-5/",
    "#category": ("", "hiperdex", "chapter"),
    "#class"   : hiperdex.HiperdexChapterExtractor,
    "#exception": exception.HttpError,
},

{
    "#url"     : "https://hiperdex.top/manga/domestic-na-kanojo/154-5/",
    "#category": ("", "hiperdex", "chapter"),
    "#class"   : hiperdex.HiperdexChapterExtractor,
    "#exception": exception.HttpError,
},

{
    "#url"     : "https://hiperdex.com/manga/the-second-coming-of-gluttony/",
    "#category": ("", "hiperdex", "manga"),
    "#class"   : hiperdex.HiperdexMangaExtractor,
    "#pattern" : hiperdex.HiperdexChapterExtractor.pattern,
    "#count"   : range(50, 200),

    "artist"       : list,
    "author"       : list,
    "chapter"      : int,
    "chapter_minor": str,
    "description"  : str,
    "manga"        : "The Second Coming of Gluttony",
    "score"        : {int, float},
    "status"       : str,
    "type"         : "manhwa",
    "year"         : 2019,
},

{
    "#url"     : "https://hiperdex.com/manga/youre-not-that-special/",
    "#category": ("", "hiperdex", "manga"),
    "#class"   : hiperdex.HiperdexMangaExtractor,
    "#exception": exception.HttpError,
},

{
    "#url"     : "https://1sthiperdex.com/manga/youre-not-that-special/",
    "#category": ("", "hiperdex", "manga"),
    "#class"   : hiperdex.HiperdexMangaExtractor,
    "#exception": exception.HttpError,
},

{
    "#url"     : "https://hiperdex2.com/manga/youre-not-that-special/",
    "#category": ("", "hiperdex", "manga"),
    "#class"   : hiperdex.HiperdexMangaExtractor,
    "#exception": exception.HttpError,
},

{
    "#url"     : "https://hiperdex.net/manga/youre-not-that-special/",
    "#category": ("", "hiperdex", "manga"),
    "#class"   : hiperdex.HiperdexMangaExtractor,
    "#exception": exception.HttpError,
},

{
    "#url"     : "https://hiperdex.info/manga/youre-not-that-special/",
    "#category": ("", "hiperdex", "manga"),
    "#class"   : hiperdex.HiperdexMangaExtractor,
    "#exception": exception.HttpError,
},

{
    "#url"     : "https://1sthiperdex.com/manga-artist/beck-ho-an/",
    "#category": ("", "hiperdex", "artist"),
    "#class"   : hiperdex.HiperdexArtistExtractor,
},

{
    "#url"     : "https://hiperdex.net/manga-artist/beck-ho-an/",
    "#category": ("", "hiperdex", "artist"),
    "#class"   : hiperdex.HiperdexArtistExtractor,
},

{
    "#url"     : "https://hiperdex2.com/manga-artist/beck-ho-an/",
    "#category": ("", "hiperdex", "artist"),
    "#class"   : hiperdex.HiperdexArtistExtractor,
},

{
    "#url"     : "https://hiperdex.info/manga-artist/beck-ho-an/",
    "#category": ("", "hiperdex", "artist"),
    "#class"   : hiperdex.HiperdexArtistExtractor,
},

{
    "#url"     : "https://hiperdex.com/manga-author/viagra/",
    "#category": ("", "hiperdex", "artist"),
    "#class"   : hiperdex.HiperdexArtistExtractor,
    "#count"   : range(0, 20),
},

)
