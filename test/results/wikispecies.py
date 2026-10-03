# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import wikimedia


__tests__ = (
{
    "#url"     : "https://species.wikimedia.org/wiki/Geranospiza",
    "#category": ("wikimedia", "wikispecies", "article"),
    "#class"   : wikimedia.WikimediaArticleExtractor,
    "#pattern"     : r"https://upload\.wikimedia\.org/wikipedia/commons/0/01/Geranospiza_caerulescens\.jpg(?:\?.*)?",
    "#count"       : 1,
},

{
    "#url"     : "https://species.wikimedia.org/wiki/Category:Names",
    "#category": ("wikimedia", "wikispecies", "category"),
    "#class"   : wikimedia.WikimediaArticleExtractor,
},

)
