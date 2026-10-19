# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import imagehosts
from gallery_dl import exception


__tests__ = (
{
    "#url"     : "https://imgadult.com/img-686b4f451af05.html",
    "#comment" : "missing image (empty 200)",
    "#class"   : imagehosts.ImgadultImageExtractor,
    "#exception": exception.NotFoundError,
},

)
