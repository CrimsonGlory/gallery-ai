# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

gallery_dl = __import__("gallery_dl.extractor.2chen")
_2chen = getattr(gallery_dl.extractor, "2chen")
from gallery_dl import exception


__tests__ = (
{
    "#url"     : "https://schan.help/tv/757",
    "#category": ("2chen", "schan", "thread"),
    "#class"   : _2chen._2chenThreadExtractor,
    "#exception": exception.NotFoundError,
},

{
    "#url"     : "https://schan.help/tv/",
    "#category": ("2chen", "schan", "board"),
    "#class"   : _2chen._2chenBoardExtractor,
    "#exception": exception.NotFoundError,
},

)
