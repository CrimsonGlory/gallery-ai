# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import imagehosts
from gallery_dl import exception


__tests__ = (
{
    "#url"     : "https://imgtaxi.com/img-61c71cea940d6.html",
    "#comment" : "missing image (empty 200, no og:image)",
    "#category": ("imagehost", "imgtaxi", "image"),
    "#class"   : imagehosts.ImgdriveImageExtractor,
    "#exception": exception.NotFoundError,
},

)
