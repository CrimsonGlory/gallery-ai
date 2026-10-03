# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import piczel
from gallery_dl import exception


__tests__ = (
{
    "#url"  : "https://piczel.tv/gallery/Bikupan",
    "#class": piczel.PiczelUserExtractor,
    "#exception": exception.HttpError,
},

{
    "#url"  : "https://piczel.tv/gallery/Lulena/1114",
    "#class": piczel.PiczelFolderExtractor,
    "#exception": exception.HttpError,
},

{
    "#url"  : "https://piczel.tv/gallery/image/7807",
    "#class": piczel.PiczelImageExtractor,
    "#exception": exception.HttpError,
},

{
    "#url"    : "https://piczel.tv/gallery/image/8008",
    "#comment": "multi; gallery API 410",
    "#class"  : piczel.PiczelImageExtractor,
    "#exception": exception.HttpError,
},

)
