# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import picazor


__tests__ = (
{
    "#url"     : "https://picazor.com/en/kailey-mae",
    "#class"   : picazor.PicazorUserExtractor,
    "#range"   : "1-50",
    "#pattern" : r"https://picazor\.com/uploads/.+\.(jpe?g|png|mp4|webm)",
    "#count"   : 50,

    "count"    : int,
    "num"      : int,
    "extension": {"jpg", "jpeg", "png", "mp4", "webm"},
    "filename" : str,
    "id"       : "re:[0-9a-f]+",
    "mime"     : {"photo", "video"},
    "path"     : str,
    "user"     : "kailey-mae",
    "visible"  : True,
    "?subject" : dict,
},

{
    "#url"     : "https://picazor.com/vi/badassnugget",
    "#comment" : "non-'en' language code",
    "#class"   : picazor.PicazorUserExtractor,
},

)
