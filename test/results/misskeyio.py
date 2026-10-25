# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import misskey


__tests__ = (
{
    "#url"     : "https://misskey.io/@lithla",
    "#category": ("misskey", "misskey.io", "user"),
    "#class"   : misskey.MisskeyUserExtractor,
    "#options" : {"include": "all"},
    "#results" : (
        "https://misskey.io/@lithla/info",
        "https://misskey.io/@lithla/avatar",
        "https://misskey.io/@lithla/banner",
        "https://misskey.io/@lithla/notes",
    ),
},

{
    "#url"     : "https://misskey.io/@lithla/notes",
    "#category": ("misskey", "misskey.io", "notes"),
    "#class"   : misskey.MisskeyNotesExtractor,
    "#pattern" : r"https://(media.misskeyusercontent.(jp|com)|s\d+\.arkjp\.net)/(misskey|io)/[\w-]+(?:\.\w+)?",
    "#range"   : "1-50",
    "#count"   : 50,
},

{
    "#url"     : "https://misskey.io/@lithla/info",
    "#category": ("misskey", "misskey.io", "info"),
    "#class"   : misskey.MisskeyInfoExtractor,
},

{
    "#url"     : "https://misskey.io/@lithla/avatar",
    "#category": ("misskey", "misskey.io", "avatar"),
    "#class"   : misskey.MisskeyAvatarExtractor,
    "#results" : "https://media.misskeyusercontent.jp/io/d84e09f8-99b7-423a-9229-78ba65ab8a82.gif",
    "#sha1_content": "375af4d302a4aef0bc8fc3f15b2c75ec952ac086",

    "extension": "gif",
    "filename" : "d84e09f8-99b7-423a-9229-78ba65ab8a82",
    "id"       : "avatar",
    "instance" : "misskey.io",
    "file"     : {"id": "d84e09f8-99b7-423a-9229-78ba65ab8a82"},
    "user"     : {"id": "9bhpt59w5k"},
},

{
    "#url"     : "https://misskey.io/@lithla/banner",
    "#category": ("misskey", "misskey.io", "background"),
    "#class"   : misskey.MisskeyBackgroundExtractor,
    "#results" : "https://media.misskeyusercontent.jp/io/314351a8-cc1a-469f-829f-09a296ce192f.gif",
    "#sha1_content": "ff17ba9eba7de617fac72abba106834865a63d43",

    "extension": "gif",
    "filename" : "314351a8-cc1a-469f-829f-09a296ce192f",
    "id"       : "background",
    "instance" : "misskey.io",
    "file"     : {"id": "314351a8-cc1a-469f-829f-09a296ce192f"},
    "user"     : {"id": "9bhpt59w5k"},
},

{
    "#url"     : "https://misskey.io/@blooddj@pawoo.net/notes",
    "#category": ("misskey", "misskey.io", "notes"),
    "#class"   : misskey.MisskeyNotesExtractor,
    "#range"   : "1-50",
    "#count"   : 50,
},

{
    "#url"     : "https://misskey.io/@blooddj@pawoo.net/following",
    "#category": ("misskey", "misskey.io", "following"),
    "#class"   : misskey.MisskeyFollowingExtractor,
    "#count"    : ">= 6",
    "#extractor": False,
},

{
    "#url"     : "https://misskey.io/notes/9bhqfo835v",
    "#category": ("misskey", "misskey.io", "note"),
    "#class"   : misskey.MisskeyNoteExtractor,
    "#results" : (
        "https://media.misskeyusercontent.jp/misskey/1cbba095-5a19-4107-8e20-3efb0456dda4.png?sensitive=true",
        "https://media.misskeyusercontent.jp/misskey/6baa558b-94ac-4bd2-a393-a52324a9d2d4.png?sensitive=true",
        "https://media.misskeyusercontent.jp/misskey/14133ad0-ea40-4fed-b6e7-65d4cbe19b96.png?sensitive=true",
        "https://media.misskeyusercontent.jp/misskey/e11164a2-9de5-4769-8c73-0ae44124b565.png?sensitive=true",
    ),
},

{
    "#url"     : "https://misskey.io/notes/9brq7z1re6",
    "#category": ("misskey", "misskey.io", "note"),
    "#class"   : misskey.MisskeyNoteExtractor,
},

{
    "#url"     : "https://misskey.io/my/favorites",
    "#category": ("misskey", "misskey.io", "favorite"),
    "#class"   : misskey.MisskeyFavoriteExtractor,
},

{
    "#url"     : "https://misskey.io/api/i/favorites",
    "#category": ("misskey", "misskey.io", "favorite"),
    "#class"   : misskey.MisskeyFavoriteExtractor,
},

{
    "#url"     : "https://misskey.io/about",
    "#category": ("misskey", "misskey.io", "emoji"),
    "#class"   : misskey.MisskeyEmojiExtractor,
    "#pattern" : r"https://media\.misskeyusercontent\.jp/(emoji|misskey|io)/.+",
    "#count"   : range(10_000, 20_000),

    "aliases"       : list,
    "count"         : range(10_000, 20_000),
    "emoji_category": str,
    "extension"     : {"jpg", "jpeg", "png", "apng", "gif", "webp"},
    "filename"      : str,
    "instance"      : "misskey.io",
    "name"          : str,
    "num"           : range(1, 20_000),
    "url"           : str,
},

)
