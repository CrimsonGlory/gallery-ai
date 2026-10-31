# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import philomena


__tests__ = (
{
    "#url"     : "https://ponybooru.org/images/1",
    "#category": ("philomena", "ponybooru", "post"),
    "#class"   : philomena.PhilomenaPostExtractor,
    "#pattern" : r"https://cdn\.ponybooru\.org/img/view/2020/7/5/1\.png",
    "#count"   : 1,

    "id"     : 1,
    "format" : "png",
    "width"  : 3000,
    "height" : 3000,
},

{
    "#url"     : "https://www.ponybooru.org/images/1",
    "#category": ("philomena", "ponybooru", "post"),
    "#class"   : philomena.PhilomenaPostExtractor,
},

{
    "#url"     : "https://ponybooru.org/search?q=cute",
    "#category": ("philomena", "ponybooru", "search"),
    "#class"   : philomena.PhilomenaSearchExtractor,
    "#range"   : "40-60",
    "#count"   : 21,
},

{
    "#url"     : "https://ponybooru.org/galleries/27",
    "#category": ("philomena", "ponybooru", "gallery"),
    "#class"   : philomena.PhilomenaGalleryExtractor,
    "#count"   : ">= 24",
},

)
