# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import pixnet
from gallery_dl import exception


__tests__ = (
{
    "#url"     : "https://albertayu773.pixnet.net/album/photo/159443828",
    "#category": ("", "pixnet", "image"),
    "#class"   : pixnet.PixnetImageExtractor,
    "#results" : "https://pimg.1px.tw/albertayu773/1522072078-2378081213.jpg",

    "blog"     : "albertayu773",
    "extension": "jpg",
    "filename" : "0 (7)",
    "id"       : 159443828,
    "user"     : "日本美少女學園",
},

{
    "#url"     : "https://albertayu773.pixnet.net/albums/15078995/photos/159443828",
    "#category": ("", "pixnet", "image"),
    "#class"   : pixnet.PixnetImageExtractor,
},

{
    "#url"     : "https://albertayu773.pixnet.net/album/set/15078995",
    "#category": ("", "pixnet", "set"),
    "#class"   : pixnet.PixnetSetExtractor,
    "#pattern" : r"https://pimg\.1px\.tw/albertayu773/[^/?#]+\.jpg",
    "#count"   : 11,

    "blog"        : "albertayu773",
    "folder_id"   : "",
    "folder_title": "",
    "set_id"      : 15078995,
    "set_title"   : "2018 NEWS(16月份)",
    "user"        : "日本美少女學園",
},

{
    "#url"     : "https://albertayu773.pixnet.net/albums/15078995",
    "#category": ("", "pixnet", "set"),
    "#class"   : pixnet.PixnetSetExtractor,
},

{
    "#url"     : "https://anrine910070.pixnet.net/album/set/5917493",
    "#comment" : "private blog",
    "#category": ("", "pixnet", "set"),
    "#class"   : pixnet.PixnetSetExtractor,
    "#exception": exception.AuthorizationError,
},

{
    "#url"     : "https://sky92100.pixnet.net/album/set/17492544",
    "#comment" : "password-protected set gone after album redesign",
    "#category": ("", "pixnet", "set"),
    "#class"   : pixnet.PixnetSetExtractor,
    "#exception": exception.NotFoundError,
},

{
    "#url"     : "https://sky92100.pixnet.net/albums/219087151",
    "#category": ("", "pixnet", "set"),
    "#class"   : pixnet.PixnetSetExtractor,
    "#pattern" : r"https://pimg\.1px\.tw/sky92100/.+",
    "#count"   : range(70, 90),
},

{
    "#url"     : "https://albertayu773.pixnet.net/album/folder/1405768",
    "#category": ("", "pixnet", "folder"),
    "#class"   : pixnet.PixnetFolderExtractor,
    "#pattern" : r"https://albertayu773\.pixnet\.net/albums/\d+",
    "#count"   : ">= 10",
},

{
    "#url"     : "https://albertayu773.pixnet.net/albums?folderId=1405768",
    "#category": ("", "pixnet", "folder"),
    "#class"   : pixnet.PixnetFolderExtractor,
},

{
    "#url"     : "https://albertayu773.pixnet.net/",
    "#category": ("", "pixnet", "user"),
    "#class"   : pixnet.PixnetUserExtractor,
},

{
    "#url"     : "https://albertayu773.pixnet.net/blog",
    "#category": ("", "pixnet", "user"),
    "#class"   : pixnet.PixnetUserExtractor,
},

{
    "#url"     : "https://albertayu773.pixnet.net/album",
    "#category": ("", "pixnet", "user"),
    "#class"   : pixnet.PixnetUserExtractor,
},

{
    "#url"     : "https://albertayu773.pixnet.net/albums",
    "#category": ("", "pixnet", "user"),
    "#class"   : pixnet.PixnetUserExtractor,
},

{
    "#url"     : "https://albertayu773.pixnet.net/album/list",
    "#category": ("", "pixnet", "user"),
    "#class"   : pixnet.PixnetUserExtractor,
    "#pattern" : r"https://albertayu773\.pixnet\.net/albums\?folderId=\d+",
    "#count"   : ">= 30",
},

{
    "#url"     : "https://anrine910070.pixnet.net/album/list",
    "#comment" : "private blog",
    "#category": ("", "pixnet", "user"),
    "#class"   : pixnet.PixnetUserExtractor,
    "#exception": exception.AuthorizationError,
},

{
    "#url"     : "https://sky92100.pixnet.net/albums",
    "#category": ("", "pixnet", "user"),
    "#class"   : pixnet.PixnetUserExtractor,
    "#pattern" : r"https://sky92100\.pixnet\.net/albums/\d+",
    "#count"   : ">= 8",
},

)
