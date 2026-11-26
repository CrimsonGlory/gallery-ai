# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import imagehosts
from gallery_dl import exception


__tests__ = (
{
    "#url"      : "https://imgspice.com/q1taxkhxprrn/58410038_cal022jsp_308191001.jpg.html",
    "#comment"  : "image gone; imgspice.com no longer hosts images",
    "#category" : ("imagehost", "imgspice", "image"),
    "#class"    : imagehosts.ImgspiceImageExtractor,
    "#exception": exception.NotFoundError,
},

)
