# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import vk
from gallery_dl import exception


__tests__ = (
{
    "#url"     : "https://vk.com/id398982326",
    "#category": ("", "vk", "photos"),
    "#class"   : vk.VkPhotosExtractor,
    "#pattern" : r"https://sun\d+-\d+\.userapi\.com/",
    "#count"   : ">= 35",

    "id"  : r"re:\d+",
    "date": "type:datetime",
    "user": {
        "group": bool,
        "id"  : "398982326",
        "info": str,
        "name": str,
        "nick": str,
    },
},

{
    "#url"     : "https://vk.ru/id398982326",
    "#class"   : vk.VkPhotosExtractor,
},

{
    "#url"     : "https://vk.com/cosplayinrussia",
    "#category": ("", "vk", "photos"),
    "#class"   : vk.VkPhotosExtractor,
    "#range"   : "15-25",

    "id"  : r"re:\d+",
    "date": "type:datetime",
    "user": {
        "group": True,
        "id"  : "-165740836",
        "info": "",
        "name": "cosplayinrussia",
        "nick": "Косплей | Cosplay 18+",
    },
},

{
    "#url"     : "https://vk.com/id76957806",
    "#comment" : "photos without width/height (#2535)",
    "#category": ("", "vk", "photos"),
    "#class"   : vk.VkPhotosExtractor,
    "#pattern" : r"https://sun\d+-\d+\.userapi\.com/",
    "#range"   : "1-9",
    "#count"   : 9,

    "date": "type:datetime",
},

{
    "#url"     : "https://m.vk.com/albums398982326",
    "#category": ("", "vk", "photos"),
    "#class"   : vk.VkPhotosExtractor,
},

{
    "#url"     : "https://www.vk.com/id398982326?profile=1",
    "#category": ("", "vk", "photos"),
    "#class"   : vk.VkPhotosExtractor,
},

{
    "#url"     : "https://vk.com/albums-165740836",
    "#category": ("", "vk", "photos"),
    "#class"   : vk.VkPhotosExtractor,
},

{
    "#url"     : "https://vk.com/album-165740836_281339889",
    "#category": ("", "vk", "album"),
    "#class"   : vk.VkAlbumExtractor,
    "#count"   : 12,
    "#log"     : "-165740836_281339889: Failed to extract metadata ('Access denied')",

    "album": {
        "id"    : "281339889",
        "!name" : str,
        "!count": int,
    },
    "user": {
        "id": "-165740836",
        "!name" : str,
        "!nick" : str,
        "!group": bool,

    },
},

{
    "#url"     : "https://vk.com/album-53775183_00",
    "#comment" : "'Access denied' (#2556)",
    "#category": ("", "vk", "album"),
    "#class"   : vk.VkAlbumExtractor,
    "#exception": exception.AuthorizationError,
},

{
    "#url"     : "https://vk.com/album232175027_00",
    "#category": ("", "vk", "album"),
    "#class"   : vk.VkAlbumExtractor,
    "#exception": exception.AuthorizationError,
},

{
    "#url"     : "https://vk.com/album-205150448_00",
    "#class"   : vk.VkAlbumExtractor,
    "#range"   : "1-25",
    "#count"   : 25,

    "id"           : r"re:\d+",
    "width"        : range(100, 8_000),
    "height"       : range(100, 8_000),
    "filename"     : str,
    "extension"    : {"jpg", "png"},
    "date"         : "type:datetime",
    "count"        : 826,
    "num"          : range(1, 25),
    "description"  : str,
    "hash"         : r"re:[0-9a-f]{18}",
    "likes"        : int,
    "album"        : {
        "id"   : "00",
        "name" : "Community wall photos",
        "count": 826,
    },
    "user"         : {
        "id"   : "-205150448",
        "name" : "otjareniy",
        "nick" : "Отжареный Овощ(16+)",
        "group": True,
    },
},

{
    "#url"     : "https://vk.com/tag304303884",
    "#category": ("", "vk", "tagged"),
    "#class"   : vk.VkTaggedExtractor,
    "#exception": exception.AuthorizationError,
},

{
    "#url"     : "https://vk.com/wall-213352498_2115",
    "#class"   : vk.VkWallPostExtractor,
    "#pattern" : r"https://sun\d+-\d+\.userapi\.com/",
    "#count"   : 6,

    "id"           : r"re:^\d+$",
    "width"        : 720,
    "height"       : 1280,
    "count"        : 6,
    "num"          : range(1, 6),
    "likes"        : int,
    "user"         : {
        "id": "-213352498",
    },
    "wall"         : {
        "description": str,
        "id"         : "2115",
    },
},

)
