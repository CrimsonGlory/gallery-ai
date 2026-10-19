# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import nitter
from gallery_dl import exception


__tests__ = (
{
    "#url"     : "https://nitter.net/supernaturepics/status/604341487988576256",
    "#comment" : "nitter.net is offline",
    "#category": ("nitter", "nitter.net", "tweet"),
    "#class"   : nitter.NitterTweetExtractor,
    "#exception": exception.AbortExtraction,
},

{
    "#url"     : "https://nitter.net/supernaturepics",
    "#category": ("nitter", "nitter.net", "tweets"),
    "#class"   : nitter.NitterTweetsExtractor,
},

)
