# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import shopify
from gallery_dl import exception


__tests__ = (
{
    "#url"     : "https://www.omgmiamiswimwear.com/collections/fajas",
    "#category": ("shopify", "omgmiamiswimwear", "collection"),
    "#class"   : shopify.ShopifyCollectionExtractor,
    "#exception": exception.HttpError,
},

{
    "#url"     : "https://www.omgmiamiswimwear.com/products/snatch-me-waist-belt",
    "#category": ("shopify", "omgmiamiswimwear", "product"),
    "#class"   : shopify.ShopifyProductExtractor,
    "#exception": exception.HttpError,
},

)
