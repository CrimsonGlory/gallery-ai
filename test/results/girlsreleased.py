# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import girlsreleased
from gallery_dl import exception


__tests__ = (
{
    "#url"      : "https://girlsreleased.com/set/32332",
    "#comment"  : "API 0.2 /set/{id} now returns a stub without set data",
    "#category" : ("", "girlsreleased", "set"),
    "#class"    : girlsreleased.GirlsreleasedSetExtractor,
    "#exception": exception.NotFoundError,
},

{
    "#url"      : "https://girlsreleased.com/set/124943",
    "#comment"  : "API 0.2 /set/{id} now returns a stub without set data",
    "#category" : ("", "girlsreleased", "set"),
    "#class"    : girlsreleased.GirlsreleasedSetExtractor,
    "#exception": exception.NotFoundError,
},

{
    "#url"     : "https://girlsreleased.com/model/11545/Ariana%20Regent",
    "#category": ("", "girlsreleased", "model"),
    "#class"   : girlsreleased.GirlsreleasedModelExtractor,
    "#pattern" : r"https://girlsreleased\.com/set/\d+",
    "#count"   : range(1, 20),
},

{
    "#url"     : "https://girlsreleased.com/site/amourangels.com",
    "#category": ("", "girlsreleased", "site"),
    "#class"   : girlsreleased.GirlsreleasedSiteExtractor,
},

{
    "#url"     : "https://girlsreleased.com/site/femjoy.com/model/854/Gabi",
    "#category": ("", "girlsreleased", "site"),
    "#class"   : girlsreleased.GirlsreleasedSiteExtractor,
    "#pattern" : girlsreleased.GirlsreleasedSetExtractor.pattern,
    "#count"   : 17,
},

)
