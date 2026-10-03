# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import rule34xyz


__tests__ = (
{
    "#url"     : "https://rule34.world/post/1280481",
    "#category": ("booru", "rule34world", "post"),
    "#class"   : rule34xyz.Rule34xyzPostExtractor,
    "#options" : {"tags": True},
    "#pattern" : r"https://rule34(\.world|storage\.b-cdn\.net)/posts/1280/1280481/1280481\.pic\.jpg",

    "created"       : "2026-03-11T21:03:11.567029Z",
    "data"          : {"sources": ["https://x.com/i/status/2031516276615499895"]},
    "date"          : "dt:2026-03-11 21:03:11",
    "extension"     : "jpg",
    "file_url"      : str,
    "filename"      : "1280481",
    "format"        : "pic",
    "format_id"     : "10",
    "height"        : 1618,
    "id"            : 1280481,
    "likes"         : int,
    "posted"        : "2026-03-11T21:08:34.291657Z",
    "status"        : 2,
    "tags_artist"   : list,
    "tags_character": list,
    "?tags_meta"    : list,
    "type"          : 0,
    "uploaderId"    : int,
    "width"         : 2047,
    "tags"          : list,
    "tags_copyright": list,
    "tags_general"  : list,
},

{
    "#url"     : "https://rule34.world/zenless_zone_zero",
    "#category": ("booru", "rule34world", "tag"),
    "#class"   : rule34xyz.Rule34xyzTagExtractor,
    "#pattern" : r"https://rule34(\.world|storage.b-cdn.net)/posts/\d+/\d+/\d+\.(pic\.jpg|mov.mp4)",
    "#range"   : "1-100",
    "#count"   : 100,

    "created"    : "iso:8601",
    "date"       : "type:datetime",
    "extension"  : {"jpg", "mp4"},
    "file_url"   : str,
    "filename"   : r"re:\d+",
    "format"     : {"pic", "mov"},
    "format_id"  : {"10", "100"},
    "width"      : int,
    "height"     : int,
    "id"         : int,
    "likes"      : int,
    "posted"     : "iso:8601",
    "search_tags": "zenless zone zero",
    "status"     : 2,
    "type"       : {0, 1},
    "uploaderId" : int,
},

{
    "#url"     : "https://rule34.world/preview_%2528preview0%2529",
    "#category": ("booru", "rule34world", "tag"),
    "#class"   : rule34xyz.Rule34xyzTagExtractor,
    "#range"   : "1-100",
    "#count"   : range(10, 40),

    "search_tags": "preview (preview0)",
},

{
    "#url"     : "https://rule34.world/playlists/view/259015",
    "#category": ("booru", "rule34world", "playlist"),
    "#class"   : rule34xyz.Rule34xyzPlaylistExtractor,
    "#count"   : range(0, 40),

    "playlist_id": "259015",
},

)
