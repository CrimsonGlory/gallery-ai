# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import nsfwalbum


__tests__ = (
{
    "#url"     : "https://nsfwalbum.com/album/401611",
    "#category": ("", "nsfwalbum", "album"),
    "#class"   : nsfwalbum.NsfwalbumAlbumExtractor,
    "#range"        : "1-5",
    "#pattern"      : r"https://.+",
    "#count"        : range(1, 6),

    "album_id" : 401611,
    "extension": "jpg",
    "filename" : str,
    "height"   : int,
    "id"       : int,
    "models"   : [],
    "num"      : range(1, 5),
    "studio"   : "Met-Art",
    "title"    : "Met-Art - Katherine A - Difuza 25.05.2014 (134 photos)(4368 X 2912)",
    "width"    : int,
},

{
    "#url"     : "https://nsfwalbum.com/album/935244",
    "#comment" : "'range' skip",
    "#class"   : nsfwalbum.NsfwalbumAlbumExtractor,
    "#range"   : "11",
    "#pattern" : r"https://images\d+\.imagebam\.com/.+/ME1BU3GD_o\.jpg",
    "#count"   : 1,

    "filename" : "ME1BU3GD_o",
    "extension": "jpg",
    "album_id" : 935244,
    "id"       : 90041058,
    "width"    : int,
    "height"   : int,
    "models"   : [],
    "num"      : 11,
    "studio"   : "Graphis",
    "title"    : "Graphis Mirei Uno - Ephemerality - Set 03 - x20",
},

{
    "#url"     : "https://nsfwalbum.com/photo/90041058",
    "#class"   : nsfwalbum.NsfwalbumImageExtractor,
    "#pattern" : r"https://images\d+\.imagebam\.com/.+/ME1BU3GD_o\.jpg",
    "#count"   : 1,

    "filename" : "ME1BU3GD_o",
    "extension": "jpg",
    "id"       : 90041058,
    "width"    : int,
    "height"   : int,
},

)
