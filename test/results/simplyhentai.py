# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import simplyhentai


__tests__ = (
{
    "#url"     : "https://www.simply-hentai.com/puella-magi-madoka-magica/hangyaku-no-hanafuda-monogatari-english",
    "#class"   : simplyhentai.SimplyhentaiGalleryExtractor,
    "#pattern" : r"https://images\.sh\-cdn\.com/0/c/1/e/365291/\w+\.jpg",
    "#count"   : 25,

    "artists"        : [],
    "?comment_count" : int,
    "count"          : 25,
    "cover"          : "https://images.sh-cdn.com/0/c/1/e/365291/1f47ed30.jpg",
    "created_at"     : str,
    "date"           : "type:datetime",
    "description"    : None,
    "extension"      : "jpg",
    "filename"       : str,
    "gallery_id"     : 365291,
    "id"             : int,
    "image_count"    : 25,
    "lang"           : "en",
    "language"       : "English",
    "?new"           : False,
    "num"            : range(1, 25),
    "other_languages": [],
    "parodies"       : ["Puella Magi Madoka Magica"],
    "?reactions"     : {},
    "redirected"     : bool,
    "series"         : "Puella Magi Madoka Magica",
    "slug"           : str,
    "title"          : "Hangyaku no Hanafuda Monogatari [English}",
    "translators"    : [],
    "type"           : "Album",
    "user"           : None,
    "views"          : range(80_000, 500_000),
    "characters"     : [
        "homura akemi",
        "kyouko sakura",
        "madoka kaname",
        "mami tomoe",
        "sayaka miki",
    ],
    "tags"           : [
        "females only",
        "Giantess",
        "Kimono",
        "Yuri",
    ],
    "?anijunky"      : dict,
    "interactions"   : dict,
    "!related"       : dict,
    "!images"        : list,
    "!pages"         : list,
},

{
    "#url"     : "https://www.simply-hentai.com/dungeon-ni-deai-o-motomeru-no-wa-machigatteiru-darou-ka/aisha-defeated-by-bell",
    "#comment" : "12 or less pages",
    "#class"   : simplyhentai.SimplyhentaiGalleryExtractor,
    "#pattern" : r"https://images\.sh\-cdn\.com/f/0/6/6/364253/\w+\.jpg",
    "#count"   : 11,

    "artists"        : ["bareisho tarou"],
    "count"          : 11,
    "cover"          : "https://images.sh-cdn.com/f/0/6/6/364253/a313a9ae.jpg",
    "date"           : "type:datetime",
    "gallery_id"     : 364253,
    "id"             : int,
    "lang"           : "en",
    "parodies"       : ["dungeon ni deai o motomeru no wa machigatteiru darou ka"],
    "series"         : "dungeon ni deai o motomeru no wa machigatteiru darou ka",
    "title"          : "Aisha Defeated By Bell",
    "characters"     : [
        "aisha belka",
        "bell cranel",
        "haruhime sanjouno",
    ],
    "tags"           : [
        "big breasts",
        "big penis",
        "Dark Skin",
        "Fox Girl",
        "Harem",
        "Impregnation",
        "kemonomimi | animal ears",
        "Kimono",
        "multi-work series",
        "Nakadashi",
        "Pregnant",
        "Prostitution",
        "sole female",
        "sole male",
        "very long hair",
    ],
},

{
    "#url"     : "https://www.simply-hentai.com/series/mysterious-girlfriend-x",
    "#class"   : simplyhentai.SimplyhentaiSeriesExtractor,
    "#pattern" : r"https://www\.simply-hentai\.com/(?:\d+-)?mysterious-girlfriend-x/(?:\d+-)?[\w-]+",
    "#count"   : range(3, 10),
},

{
    "#url"     : "https://www.simply-hentai.com/series/mysterious-girlfriend-x/tag-nakadashi/sort-popularity",
    "#class"   : simplyhentai.SimplyhentaiSeriesExtractor,
    "#pattern" : r"https://www\.simply-hentai\.com/(?:\d+-)?mysterious-girlfriend-x/(?:\d+-)?[\w-]+",
    "#count"   : range(1, 10),
},

{
    "#url"     : "https://www.simply-hentai.com/series/mysterious-girlfriend-x?filter%5Btags%5D%5B0%5D=schoolgirl%20uniform&filter%5Btags%5D%5B1%5D=Nakadashi&filter%5Bparodies%5D%5B0%5D=Nazo%20no%20Kanojo%20X",
    "#class"   : simplyhentai.SimplyhentaiSeriesExtractor,
    "#pattern" : r"https://www\.simply-hentai\.com/(?:\d+-)?mysterious-girlfriend-x/(?:\d+-)?sekkyokuteki-na-kanojo",
    "#count"   : range(1, 5),
},

{
    "#url"     : "https://www.simply-hentai.com/2-mangas",
    "#class"   : simplyhentai.SimplyhentaiMangaExtractor,
    "#pattern" : simplyhentai.SimplyhentaiGalleryExtractor.pattern,
    "#range"   : "1-5",
},

{
    "#url"     : "https://www.simply-hentai.com/2-mangas/sort-most-viewed",
    "#class"   : simplyhentai.SimplyhentaiMangaExtractor,
    "#range"   : "1-5",
    "#pattern" : simplyhentai.SimplyhentaiGalleryExtractor.pattern,
    "#count"   : 5,
},

{
    "#url"     : "https://www.simply-hentai.com/language/polish",
    "#class"   : simplyhentai.SimplyhentaiLanguageExtractor,
    "#pattern" : simplyhentai.SimplyhentaiGalleryExtractor.pattern,
    "#count"   : range(1, 20),
},

{
    "#url"     : "https://www.simply-hentai.com/language/german/sort-newest/page-12",
    "#class"   : simplyhentai.SimplyhentaiLanguageExtractor,
    "#pattern" : simplyhentai.SimplyhentaiGalleryExtractor.pattern,
    "#count"   : 12,
},

{
    "#url"     : "https://www.simply-hentai.com/parody/touhou",
    "#class"   : simplyhentai.SimplyhentaiTagExtractor,
},

{
    "#url"     : "https://www.simply-hentai.com/tag/1-sole-female",
    "#class"   : simplyhentai.SimplyhentaiTagExtractor,
},

{
    "#url"     : "https://www.simply-hentai.com/character/producer",
    "#class"   : simplyhentai.SimplyhentaiTagExtractor,
},

{
    "#url"     : "https://www.simply-hentai.com/collection/english-b5e31",
    "#class"   : simplyhentai.SimplyhentaiTagExtractor,
    "#pattern" : simplyhentai.SimplyhentaiGalleryExtractor.pattern,
    "#count"   : range(1, 10),
},

{
    "#url"     : "https://www.simply-hentai.com/artist/crimson-carmine/tag-color/sort-alphabetical",
    "#class"   : simplyhentai.SimplyhentaiTagExtractor,
    "#pattern" : simplyhentai.SimplyhentaiGalleryExtractor.pattern,
    "#count"   : range(1, 200),
},

{
    "#url"     : "https://www.simply-hentai.com/translator/10-team-vanilla",
    "#class"   : simplyhentai.SimplyhentaiTagExtractor,
},

)
