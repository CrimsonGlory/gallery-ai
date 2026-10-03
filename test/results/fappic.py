# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import imagehosts
from gallery_dl import exception


__tests__ = (
{
    "#url"     : "https://fappic.com/98wxqcklyh8k/test.png",
    "#category": ("imagehost", "fappic", "image"),
    "#class"   : imagehosts.FappicImageExtractor,
},

{
    "#url"     : "https://www.fappic.com/98wxqcklyh8k/foo.bar",
    "#category": ("imagehost", "fappic", "image"),
    "#class"   : imagehosts.FappicImageExtractor,
    "#pattern"      : r"https://img\d+\.fappic\.com/img/\w+/test\.png",
    "#sha1_content" : (
        "0c8768055e4e20e7c7259608b67799171b691140",
        "c87959a90dc2cfe33920a4e43742f1ce3d778ae9",
    ),

    "filename"   : "test",
    "extension"  : "png",
    "token"      : "98wxqcklyh8k",
},

{
    "#url"     : "https://www.fappic.com/i/00133/qi2nplzmwq7d_t.jpg",
    "#comment" : "thumbnail URL (#8013)",
    "#category": ("imagehost", "fappic", "image"),
    "#class"   : imagehosts.FappicImageExtractor,
    "#exception": exception.NotFoundError,
},

)
