# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import chevereto


__tests__ = (
{
    "#url"     : "https://freeimage.host/i/loca5.n8zcqQV",
    "#comment" : "filename is '{title} [{id}].{extension}'",
    "#category": ("chevereto", "freeimagehost", "file"),
    "#class"   : chevereto.CheveretoFileExtractor,
    "#results"     : "https://iili.io/n8zcqQV.png",
    "#sha1_content": "780afaa282b1d10a45a8db748bb1de5c49d284a9",

    "album"     : "",
    "album_id"  : "",
    "album_slug": "",
    "date"      : "dt:2026-10-28 22:40:26",
    "extension" : "png",
    "filename"  : "loca5",
    "id"        : "n8zcqQV",
    "title"     : "loca5",
    "type"      : "article",
    "url"       : "https://iili.io/n8zcqQV.png",
    "user"      : "",
},

{
    "#url"     : "https://freeimage.host/i/n8zcqQV",
    "#comment" : "image ID without name",
    "#category": ("chevereto", "freeimagehost", "file"),
    "#class"   : chevereto.CheveretoFileExtractor,
    "#results" : "https://iili.io/n8zcqQV.png",

    "extension": "png",
    "filename" : "loca5",
    "id"       : "n8zcqQV",
    "title"    : "loca5",
    "url"      : "https://iili.io/n8zcqQV.png",
},

{
    "#url"     : "https://www.freeimage.host/i/loca5.n8zcqQV",
    "#category": ("chevereto", "freeimagehost", "file"),
    "#class"   : chevereto.CheveretoFileExtractor,
},

{
    "#url"     : "https://freeimage.host/a/a.HouLu4",
    "#category": ("chevereto", "freeimagehost", "album"),
    "#class"   : chevereto.CheveretoAlbumExtractor,
},

{
    "#url"     : "https://freeimage.host/annasubal",
    "#category": ("chevereto", "freeimagehost", "user"),
    "#class"   : chevereto.CheveretoUserExtractor,
},

)
