# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

gallery_dl = __import__("gallery_dl.extractor.4chan")
_4chan = getattr(gallery_dl.extractor, "4chan")
from gallery_dl import exception


__tests__ = (
{
    "#url"     : "https://boards.4chan.org/tg/thread/15396072/",
    "#category": ("", "4chan", "thread"),
    "#class"   : _4chan._4chanThreadExtractor,
    "#exception": exception.HttpError,
},

{
    "#url"     : "https://boards.4channel.org/tg/thread/15396072/",
    "#category": ("", "4chan", "thread"),
    "#class"   : _4chan._4chanThreadExtractor,
    "#exception": exception.HttpError,
},

{
    "#url"     : "https://boards.4chan.org/wg/thread/8010591",
    "#comment" : "file contents filled with null bytes (#7883); thread 404",
    "#class"   : _4chan._4chanThreadExtractor,
    "#exception": exception.HttpError,
},

{
    "#url"     : "https://boards.4channel.org/po/",
    "#category": ("", "4chan", "board"),
    "#class"   : _4chan._4chanBoardExtractor,
    "#pattern" : _4chan._4chanThreadExtractor.pattern,
    "#count"   : ">= 100",
},

)
