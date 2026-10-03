# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import uploadir
from gallery_dl import exception


__tests__ = (
{
    "#url"     : "https://uploadir.com/u/rd3t46ry",
    "#comment" : "image; file gone",
    "#category": ("", "uploadir", "file"),
    "#class"   : uploadir.UploadirFileExtractor,
    "#exception": exception.NotFoundError,

    "extension": "jpg",
    "filename" : "Chloe and Rachel 4K jpg",
    "id"       : "rd3t46ry",
},

{
    "#url"     : "https://uploadir.com/uploads/gxe8ti9v/downloads/new",
    "#comment" : "archive; file gone",
    "#category": ("", "uploadir", "file"),
    "#class"   : uploadir.UploadirFileExtractor,
    "#exception": exception.NotFoundError,

    "extension": "zip",
    "filename" : "NYAN-Mods-Pack#1",
    "id"       : "gxe8ti9v",
},

{
    "#url"     : "https://uploadir.com/u/fllda6xl",
    "#comment" : "utf-8 filename; file gone",
    "#category": ("", "uploadir", "file"),
    "#class"   : uploadir.UploadirFileExtractor,
    "#exception": exception.NotFoundError,

    "extension": "png",
    "filename" : "_圖片_🖼_image_",
    "id"       : "fllda6xl",
},

{
    "#url"     : "https://uploadir.com/uploads/rd3t46ry",
    "#category": ("", "uploadir", "file"),
    "#class"   : uploadir.UploadirFileExtractor,
    "#exception": exception.NotFoundError,
},

{
    "#url"     : "https://uploadir.com/user/uploads/rd3t46ry",
    "#category": ("", "uploadir", "file"),
    "#class"   : uploadir.UploadirFileExtractor,
    "#exception": exception.NotFoundError,
},

)
