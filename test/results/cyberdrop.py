# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import cyberdrop


__tests__ = (
{
    "#url"     : "https://cyberdrop.cr/a/8uE0wQiK",
    "#comment" : "album files removed",
    "#category": ("lolisafe", "cyberdrop", "album"),
    "#class"   : cyberdrop.CyberdropAlbumExtractor,
    "#count"   : 0,

    "album_id"     : "8uE0wQiK",
    "album_name"   : """test テスト "&>""",
    "count"        : 0,
    "date"         : "dt:2023-11-26 00:00:00",
    "description"  : """test テスト "&>""",
},

{
    "#url"     : "https://cyberdrop.cr/a/HriMgbuf",
    "#comment" : "two of three album files removed",
    "#category": ("lolisafe", "cyberdrop", "album"),
    "#class"   : cyberdrop.CyberdropAlbumExtractor,
    "#pattern" : r"https://(?:k1-cd\.cdn\.gigachad-cdn\.ru|cdn\.cyberdrop\.cr)/api/file/d/urLPkBXGuNfEg\?token=ey.+",
    "#count"   : 1,

    "album_id"     : "HriMgbuf",
    "album_name"   : "animations",
    "album_size"   : int,
    "auth_url"     : r"re:https://api.cyberdrop.cr/api/file/auth/\w+",
    "count"        : 1,
    "date"         : "dt:2023-11-26 00:00:00",
    "description"  : "animated stuff",
    "extension"    : {"gif", "webm"},
    "filename"     : str,
    "id"           : str,
    "name"         : str,
    "num"          : 1,
    "size"         : int,
    "slug"         : str,
    "thumbnail_url": r"re:https://api.cyberdrop.cr/api/proxy/thumb/\w+",
    "type"         : {"image/gif", "video/webm"},
    "url"          : str,
},

{
    "#url"     : "https://cyberdrop.me/a/8uE0wQiK",
    "#category": ("lolisafe", "cyberdrop", "album"),
    "#class"   : cyberdrop.CyberdropAlbumExtractor,
},

{
    "#url"     : "https://cyberdrop.cr/f/rln0wNQSY5iuA",
    "#comment" : "file removed",
    "#category": ("lolisafe", "cyberdrop", "media"),
    "#class"   : cyberdrop.CyberdropMediaExtractor,
    "#count"   : 0,

    "album_id"     : "",
    "album_name"   : "",
    "album_size"   : -1,
    "count"        : 1,
    "description"  : "",
},

{
    "#url"     : "https://cyberdrop.me/f/lHYBt9VAluZf6",
    "#category": ("lolisafe", "cyberdrop", "media"),
    "#class"   : cyberdrop.CyberdropMediaExtractor,
},

{
    "#url"     : "https://cyberdrop.me/e/lHYBt9VAluZf6",
    "#category": ("lolisafe", "cyberdrop", "media"),
    "#class"   : cyberdrop.CyberdropMediaExtractor,
},

)
