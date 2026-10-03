# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import reactor


__tests__ = (
{
    "#url"     : "http://pornreactor.cc/tag/RiceGnat",
    "#category": ("reactor", "pornreactor", "tag"),
    "#class"   : reactor.ReactorTagExtractor,
    "#range"   : "1-25",
    "#count"   : ">= 25",
},

{
    "#url"     : "http://fapreactor.com/tag/RiceGnat",
    "#category": ("reactor", "pornreactor", "tag"),
    "#class"   : reactor.ReactorTagExtractor,
},

{
    "#url"     : "http://pornreactor.cc/search?q=ecchi+hentai",
    "#category": ("reactor", "pornreactor", "search"),
    "#class"   : reactor.ReactorSearchExtractor,
},

{
    "#url"     : "http://fapreactor.com/search/ecchi+hentai",
    "#category": ("reactor", "pornreactor", "search"),
    "#class"   : reactor.ReactorSearchExtractor,
},

{
    "#url"     : "http://pornreactor.cc/user/Disillusion",
    "#category": ("reactor", "pornreactor", "user"),
    "#class"   : reactor.ReactorUserExtractor,
    "#range"   : "1-25",
    "#count"   : ">= 20",
},

{
    "#url"     : "http://fapreactor.com/user/Disillusion",
    "#category": ("reactor", "pornreactor", "user"),
    "#class"   : reactor.ReactorUserExtractor,
},

{
    "#url"     : "http://pornreactor.cc/post/863166",
    "#category": ("reactor", "pornreactor", "post"),
    "#class"   : reactor.ReactorPostExtractor,
    "#pattern"     : r"https?://.+\.(jpe?g|png|gif|webp)",
    "#count"       : ">= 1",
},

{
    "#url"     : "http://fapreactor.com/post/863166",
    "#category": ("reactor", "pornreactor", "post"),
    "#class"   : reactor.ReactorPostExtractor,
    "#pattern": r"https?://.+\.(jpe?g|png|gif|webp)",
    "#count"  : ">= 1",
},

)
