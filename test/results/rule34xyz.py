# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import rule34xyz


__tests__ = (
{
    "#url"  : "https://rule34.xyz/sfw",
    "#class": rule34xyz.Rule34xyzTagExtractor,
    "#pattern": r"https://rule34(\.xyz|xyz\.b-cdn\.net)/posts/\d+/\d+/\d+\.(pic|mov\d*)\.(jpg|mp4)",
    "#range"  : "1-150",
    "#count"  : 150,

    "search_tags": "sfw",
},

{
    "#url"     : "https://www.rule34.xyz/sfw",
    "#comment" : "URL with 'www' subdomain (#8875)",
    "#class"   : rule34xyz.Rule34xyzTagExtractor,
},

{
    "#url"  : "https://rule34.xyz/playlists/view/119",
    "#class": rule34xyz.Rule34xyzPlaylistExtractor,
    "#pattern": r"https://rule34(\.xyz|xyz\.b-cdn\.net)/posts/\d+/\d+/\d+\.(pic|mov\d*)\.(jpg|mp4)",
    "#count"  : 64,

    "playlist_id": "119",
},

{
    "#url"    : "https://rule34.xyz/post/3613851",
    "#comment": "image",
    "#class"  : rule34xyz.Rule34xyzPostExtractor,
    "#options"     : {"tags": True},
    "#results"     : "https://rule34xyz.b-cdn.net/posts/3613/3613851/3613851.pic.jpg",
    "#sha1_content": "4d7146db258fd5b1645a1a5fc01550d102f495e1",

    "created"   : "2023-03-29T03:00:59.136819Z",
    "date"      : "dt:2023-03-29 03:00:59",
    "extension" : "jpg",
    "file_url"  : "https://rule34xyz.b-cdn.net/posts/3613/3613851/3613851.pic.jpg",
    "filename"  : "3613851",
    "format"    : "pic",
    "format_id" : "10",
    "id"        : 3613851,
    "likes"     : range(3, 100),
    "posted"    : "2023-03-29T03:01:07.900161Z",
    "type"      : 0,
    "?uploaderId": 9741,
    "views"     : range(200, 2000),
    "status"    : 2,
    "data"      : {
        "sources": [
            "https://twitter.com/DesireDelta13/status/1636502494292373505?t=OrmlnC85cELyY5BPmBy9Hw&s=19",
        ],
    },
    "tags": list,
    "tags_artist": list,
    "tags_character": list,
    "tags_copyright": list,
    "tags_general": list,
    "?uploaderId"  : 9741,
},

{
    "#url"    : "https://rule34.xyz/post/3571567",
    "#comment": "video",
    "#class"  : rule34xyz.Rule34xyzPostExtractor,
    "#results"     : "https://rule34xyz.b-cdn.net/posts/3571/3571567/3571567.mov720.mp4",
    "#sha1_content": "c0a5e7e887774f91527f00e6142c435a3c482c1f",

    "format"   : "mov720",
    "format_id": "101",
},

{
    "#url"    : "https://rule34.xyz/post/3571567",
    "#comment": "'format' option",
    "#class"  : rule34xyz.Rule34xyzPostExtractor,
    "#options": {"format": "10,4,5"},
    "#results": "https://rule34xyz.b-cdn.net/posts/3571/3571567/3571567.pic.jpg",

    "format"   : "pic",
    "format_id": "10",
},

)
