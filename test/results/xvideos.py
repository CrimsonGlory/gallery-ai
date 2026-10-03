# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import xvideos
from gallery_dl import exception


__tests__ = (
{
    "#url"     : "https://www.xvideos.com/profiles/pervertedcouple/photos/751031",
    "#category": ("", "xvideos", "gallery"),
    "#class"   : xvideos.XvideosGalleryExtractor,
    "#exception": exception.NotFoundError,

    "gallery": {
        "id"   : 751031,
        "title": "Random Stuff",
        "tags" : list,
    },
    "user"   : {
        "id"         : 20245371,
        "name"       : "pervertedcouple",
        "display"    : "Pervertedcouple",
        "sex"        : "Woman",
        "description": str,
    },
},

{
    "#url"     : "https://www.xvideos.com/amateur-channels/pervertedcouple/photos/12",
    "#category": ("", "xvideos", "gallery"),
    "#class"   : xvideos.XvideosGalleryExtractor,
},

{
    "#url"     : "https://www.xvideos.com/model-channels/pervertedcouple/photos/12",
    "#category": ("", "xvideos", "gallery"),
    "#class"   : xvideos.XvideosGalleryExtractor,
},

{
    "#url"     : "https://www.xvideos.com/channels/pervertedcouple/photos/12",
    "#comment" : "/channels/ URL (#5244)",
    "#category": ("", "xvideos", "gallery"),
    "#class"   : xvideos.XvideosGalleryExtractor,
},

{
    "#url"     : "https://www.xvideos.com/model-channels/little-caprice",
    "#category": ("", "xvideos", "user"),
    "#class"   : xvideos.XvideosUserExtractor,
    "#pattern"      : r"https://www\.xvideos\.com/profiles/little-caprice/photos/\d+",
    "#count"        : range(1, 50),
},

{
    "#url"     : "https://www.xvideos.com/profiles/pervertedcouple#_tabPhotos",
    "#category": ("", "xvideos", "user"),
    "#class"   : xvideos.XvideosUserExtractor,
},

{
    "#url"     : "https://www.xvideos.com/channels/pervertedcouple",
    "#category": ("", "xvideos", "user"),
    "#class"   : xvideos.XvideosUserExtractor,
},

{
    "#url"     : "https://www.xvideos.com/amateur-channels/pervertedcouple",
    "#category": ("", "xvideos", "user"),
    "#class"   : xvideos.XvideosUserExtractor,
},

{
    "#url"     : "https://www.xvideos.com/model-channels/pervertedcouple",
    "#category": ("", "xvideos", "user"),
    "#class"   : xvideos.XvideosUserExtractor,
},

)
