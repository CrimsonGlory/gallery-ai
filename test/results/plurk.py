# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import plurk


__tests__ = (
{
    "#url"     : "https://www.plurk.com/NetKidz",
    "#category": ("", "plurk", "timeline"),
    "#class"   : plurk.PlurkTimelineExtractor,
    "#pattern" : r"https://(?:(?:images|imgs)\.plurk\.com/\w+|pbs\.twimg\.com/.+|s\.yimg\.com/.+|blogger\.googleusercontent\.com/.+)",
    "#range"   : "1-20",
    "#count"   : range(1, 21),
},

{
    "#url"     : "https://www.plurk.com/p/i701j1",
    "#category": ("", "plurk", "post"),
    "#class"   : plurk.PlurkPostExtractor,
    "#count"   : range(1, 10),
    "#pattern" : r"https?://.+",
},

{
    "#url"     : "https://www.plurk.com/p/i701j1",
    "#category": ("", "plurk", "post"),
    "#class"   : plurk.PlurkPostExtractor,
    "#options" : {"comments": True},
    "#count"   : range(1, 400),
    "#pattern" : r"https?://.+",
},

)
