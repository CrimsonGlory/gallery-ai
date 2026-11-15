# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import vanlifetrader
from gallery_dl import exception


__tests__ = (
{
    "#url"     : "https://vanlifetrader.com/listing/untrapped-solutions-new-build-mercedes-sprinter-144-awd-a2738b/",
    "#comment" : "listing removed",
    "#class"   : vanlifetrader.VanlifetraderListingExtractor,
    "#exception": exception.NotFoundError,
},

{
    "#url"     : "https://vanlifetrader.com/listing/2026-geotrek-flatiron-ascent-mercedes-sprinter-144-awd-89fec0/",
    "#class"   : vanlifetrader.VanlifetraderListingExtractor,
    "#pattern" : r"https://vanlifetrader\.com/wp\-content/uploads/\d{4}/\d{2}/.+",
    "#count"   : range(1, 100),

    "date"      : "type:datetime",
    "extension" : str,
    "filename"  : str,
    "listing_id": 403606,
    "media_id"  : int,
    "num"       : range(1, 100),
    "slug"      : "2026-geotrek-flatiron-ascent-mercedes-sprinter-144-awd-89fec0",
    "title"     : "2026 Geotrek Flatiron Ascent | Mercedes Sprinter 144 AWD",
},

{
    "#url"     : "https://vanlifetrader.com/explore/",
    "#class"   : vanlifetrader.VanlifetraderExploreExtractor,
    "#pattern" : vanlifetrader.VanlifetraderListingExtractor.pattern,
    "#count"   : ">= 1",
},

)
