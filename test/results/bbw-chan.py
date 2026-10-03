# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import lynxchan
from gallery_dl import exception


__tests__ = (
{
    "#url"     : "https://bbw-chan.link/bbwdraw/res/499.html",
    "#category": ("lynxchan", "bbw-chan", "thread"),
    "#class"   : lynxchan.LynxchanThreadExtractor,
    "#exception": exception.HttpError,
},

{
    "#url"     : "https://bbw-chan.nl/bbwdraw/res/489.html",
    "#category": ("lynxchan", "bbw-chan", "thread"),
    "#class"   : lynxchan.LynxchanThreadExtractor,
},

{
    "#url"     : "https://bbw-chan.link/bbwdraw/",
    "#category": ("lynxchan", "bbw-chan", "board"),
    "#class"   : lynxchan.LynxchanBoardExtractor,
    "#pattern" : lynxchan.LynxchanThreadExtractor.pattern,
    "#count"   : ">= 100",
},

{
    "#url"     : "https://bbw-chan.nl/bbwdraw/2.html",
    "#category": ("lynxchan", "bbw-chan", "board"),
    "#class"   : lynxchan.LynxchanBoardExtractor,
},

)
