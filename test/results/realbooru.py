# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import realbooru


__tests__ = (
{
    "#url"     : "https://realbooru.com/index.php?page=post&s=list&tags=wine",
    "#category": ("booru", "realbooru", "tag"),
    "#class"   : realbooru.RealbooruTagExtractor,
    "#count"   : ">= 64",
},

{
    "#url"     : "https://realbooru.com/index.php?page=pool&s=show&id=1",
    "#category": ("booru", "realbooru", "pool"),
    "#class"   : realbooru.RealbooruPoolExtractor,
    "#pattern" : r"https://(?:video-cdn\.)?realbooru\.com//images/[0-9a-f]{2}/[0-9a-f]{2}/[0-9a-f]{32}\.mp4",
    "#count"   : 3,
},

{
    "#url"     : "https://realbooru.com/index.php?page=favorites&s=view&id=274",
    "#category": ("booru", "realbooru", "favorite"),
    "#class"   : realbooru.RealbooruFavoriteExtractor,
    "#results" : "https://realbooru.com//images/20/3e/203eefb39f54de049e30ff788a022ac7.jpeg",
},

{
    "#url"     : "https://realbooru.com/index.php?page=post&s=view&id=862054",
    "#comment" : "regular post",
    "#category": ("booru", "realbooru", "post"),
    "#class"   : realbooru.RealbooruPostExtractor,
    "#results"     : "https://realbooru.com//images/8a/34/8a345820da989637c21ac013d522bf69.jpeg",
    "#sha1_content": "f6213e6f25c3cb9e3cfefa6d4b3a78e44b9dea5b",

    "created_at"    : "Jan, 18 2024",
    "date"          : "dt:2024-01-18 00:00:00",
    "file_url"      : "https://realbooru.com//images/8a/34/8a345820da989637c21ac013d522bf69.jpeg",
    "filename"      : "8a345820da989637c21ac013d522bf69",
    "id"            : "862054",
    "md5"           : "8a345820da989637c21ac013d522bf69",
    "rating"        : "e",
    "score"         : r"re:\d+",
    "source"        : "https://www.instagram.com/p/CwAO1UyJBnw",
    "tags"          : str,
    "tags_copyright": "instagram",
    "tags_general"  : str,
    "tags_metadata" : str,
    "tags_model"    : "kurita_emi",
},

{
    "#url"     : "https://realbooru.com/index.php?page=post&s=view&id=568145",
    "#comment" : "older post",
    "#category": ("booru", "realbooru", "post"),
    "#class"   : realbooru.RealbooruPostExtractor,
    "#sha1_content": "4a7424810f5f846c161b5d3b7c8b0a85a03368c8",
},

{
    "#url"     : "https://realbooru.com/index.php?page=post&s=view&id=825911",
    "#comment" : "animated GIF",
    "#category": ("booru", "realbooru", "post"),
    "#class"   : realbooru.RealbooruPostExtractor,
    "#results" : "https://realbooru.com//images/a3/9b/a39bfe5ea07f132db486e118b598c66c.gif",

    "created_at"   : "Feb, 19 2023",
    "date"         : "dt:2023-02-19 00:00:00",
    "extension"    : "gif",
    "file_url"     : "https://realbooru.com//images/a3/9b/a39bfe5ea07f132db486e118b598c66c.gif",
    "_fallback"    : (),
    "filename"     : "a39bfe5ea07f132db486e118b598c66c",
    "id"           : "825911",
    "md5"          : "a39bfe5ea07f132db486e118b598c66c",
    "rating"       : "e",
    "score"        : r"re:\d+",
    "source"       : "",
    "title"        : "",
    "uploader"     : "freakyguro",
    "tags"         : str,
    "tags_general" : str,
    "tags_metadata": str,
    "tags_model"   : "obokozu",
},

{
    "#url"     : "https://realbooru.com/index.php?page=post&s=view&id=751237",
    "#comment" : "video",
    "#category": ("booru", "realbooru", "post"),
    "#class"   : realbooru.RealbooruPostExtractor,
    "#pattern" : r"https://(?:video-cdn\.)?realbooru\.com//images/3c/34/3c343385126c90a7fdbccc58d342a511\.(mp4|webm)",

    "created_at"    : "Dec, 07 2020",
    "date"          : "dt:2020-12-07 00:00:00",
    "extension"     : "mp4",
    "file_url"      : str,
    "_fallback"     : ("https://realbooru.com//images/3c/34/3c343385126c90a7fdbccc58d342a511.webm",),
    "filename"      : "3c343385126c90a7fdbccc58d342a511",
    "id"            : "751237",
    "md5"           : "3c343385126c90a7fdbccc58d342a511",
    "rating"        : "e",
    "score"         : r"re:\d+",
    "source"        : "",
    "title"         : "",
    "uploader"      : "Rock 7800",
    "tags"          : str,
    "tags_copyright": str,
    "tags_general"  : str,
    "tags_metadata" : str,
    "tags_model"    : str,
},

)
