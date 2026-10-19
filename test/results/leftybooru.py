# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import leftybooru


__tests__ = (
{
    "#url"     : "https://lefty.pictures/post/view/100",
    "#category": ("shimmie2", "leftybooru", "post"),
    "#class"   : leftybooru.LeftybooruPostExtractor,
    "#pattern" : r"https://lefty\.pictures/_images/0c5838437f4c36b9cee0ee6743883089/.+\.png",

    "date"     : "dt:2015-10-21 17:18:09",
    "duration" : "",
    "extension": "png",
    "file_url" : r"re:https://lefty\.pictures/_images/0c5838437f4c36b9cee0ee6743883089/.+\.png",
    "filename" : str,
    "height"   : 1892,
    "id"       : 100,
    "md5"      : "0c5838437f4c36b9cee0ee6743883089",
    "parent_id": None,
    "rating"   : "s",
    "score"    : "0",
    "size"     : 820224,
    "source"   : None,
    "type"     : "image/png",
    "uploader" : "moe-anarchist",
    "width"    : 1375,
    "tags"     : list,
},

{
    "#url"     : "https://lefty.pictures/post/view/23042?search=meta%3Avideo",
    "#comment" : "video",
    "#category": ("shimmie2", "leftybooru", "post"),
    "#class"   : leftybooru.LeftybooruPostExtractor,
    "#pattern" : r"https://lefty\.pictures/_images/a7f4b90646a5dbf0b0a6dfab305fa5f1/.+\.mp4",

    "date"     : "dt:2024-06-18 10:40:50",
    "duration" : "16s",
    "extension": "mp4",
    "file_url" : r"re:https://lefty\.pictures/_images/a7f4b90646a5dbf0b0a6dfab305fa5f1/.+\.mp4",
    "filename" : str,
    "height"   : 1040,
    "id"       : 23042,
    "md5"      : "a7f4b90646a5dbf0b0a6dfab305fa5f1",
    "parent_id": None,
    "rating"   : "s",
    "score"    : "0",
    "size"     : 5452595,
    "source"   : "Ants (1998)",
    "type"     : "video/mp4",
    "uploader" : "vbee",
    "width"    : 1920,
    "tags"     : list,
},

{
    "#url"     : "https://lefty.pictures/post/list/vodka/1",
    "#category": ("shimmie2", "leftybooru", "tag"),
    "#class"   : leftybooru.LeftybooruTagExtractor,
    "#pattern" : r"https://lefty\.pictures/_images/[0-9a-f]{32}/\d+",
    "#count"   : 52,

    "extension"  : {"jpeg", "png", "mp4", ""},
    "file_url"   : str,
    "filename"   : str,
    "height"     : int,
    "id"         : int,
    "md5"        : "hash:md5",
    "rating"     : {"s", "q", "e"},
    "search_tags": "vodka",
    "size"       : int,
    "type"       : str,
    "width"      : int,
    "tags"       : list
},

{
    "#url"     : "https://lefty.pictures/post/list/alcohol/4",
    "#category": ("shimmie2", "leftybooru", "tag"),
    "#class"   : leftybooru.LeftybooruTagExtractor,
    "#count"   : range(30, 48),
},

{
    "#url"     : "https://lefty.pictures/post/list/1",
    "#category": ("shimmie2", "leftybooru", "tag"),
    "#class"   : leftybooru.LeftybooruTagExtractor,
},

)
