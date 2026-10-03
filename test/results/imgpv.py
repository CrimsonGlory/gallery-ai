# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import imagehosts
from gallery_dl import exception


__tests__ = (
{
    "#url"     : "https://imgpv.com/30zydqn6y1yk/4bi%20(1).jpg.html",
    "#category": ("imagehost", "imgpv", "image"),
    "#class"   : imagehosts.ImgpvImageExtractor,
    "#pattern" : r"https://s1.imgpv.com/cgi-bin/dl.cgi/xyhr\w+/4bi %26%2340%3B1%26%2341%3B.jpg",

    "date"     : "dt:2025-12-16 14:59:51",
    "extension": "jpg",
    "filename" : "4bi (1)",
    "post_url" : "https://imgpv.com/30zydqn6y1yk/4bi%20(1).jpg.html",
    "token"    : "30zydqn6y1yk",
    "user"     : "kris85",
},

{
    "#url"     : "https://imgpv.com/4sizkvumyh8v/test-%E3%83%86%E3%82%B9%E3%83%88-%22%2526%3E.jpg.html",
    "#category": ("imagehost", "imgpv", "image"),
    "#class"   : imagehosts.ImgpvImageExtractor,
    "#exception": exception.NotFoundError,
},

)
