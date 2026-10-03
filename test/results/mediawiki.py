# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import wikimedia


__tests__ = (
{
    "#url"     : "https://www.mediawiki.org/wiki/Help:Navigation",
    "#category": ("wikimedia", "mediawiki", "help"),
    "#class"   : wikimedia.WikimediaArticleExtractor,
    "#pattern" : r"https://upload\.wikimedia\.org/wikipedia/commons/.+",
    "#count"   : range(3, 20),
},

)
