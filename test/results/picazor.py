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
    "#pattern" : r"https://picazor\.com/uploads/.+\.jpg",
    "#count"   : 50,

    "count"    : range(1180, 2000),
    "num"      : range(1100, 2000),
    "extension": "jpg",
    "filename" : str,
    "id"       : "re:[0-9a-f]+",
    "mime"     : "photo",
    "path"     : str,
    "user"     : "kailey-mae",
    "userId"   : "647faf5ab6b27738234036f0",
    "visible"  : True,
},

{
    "#url"     : "https://picazor.one/en/kailey-mae",
    "#comment" : "'.one' TLD",
    "#class"   : picazor.PicazorUserExtractor,
},

{
    "#url"     : "https://picazor.com/vi/badassnugget",
    "#comment" : "non-'en' language code",
    "#class"   : picazor.PicazorUserExtractor,
},

)
