# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import imagehosts


__tests__ = (
{
    "#url"     : "https://fastpic.org/view/1/2009/1003/0c3dfd079063b645fd6afb29d2df9b7b.jpeg.html",
    "#category": ("imagehost", "fastpic", "image"),
    "#class"   : imagehosts.FastpicImageExtractor,
    "#pattern" : r"https://i1.fastpic.org/big/2009/1003/7b/0c3dfd079063b645fd6afb29d2df9b7b.jpeg\?md5=[^&#]+&expires=\d+",

    "extension": "jpeg",
    "filename" : "0c3dfd079063b645fd6afb29d2df9b7b",
    "post_url" : "https://fastpic.org/view/1/2009/1003/0c3dfd079063b645fd6afb29d2df9b7b.jpeg.html",
    "token"    : "0c3dfd079063b645fd6afb29d2df9b7b",
},

)
