# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import shopify
from gallery_dl import exception


__tests__ = (
{
    "#url"     : "https://www.fashionnova.com/collections/mini-dresses",
    "#category": ("shopify", "fashionnova", "collection"),
    "#class"   : shopify.ShopifyCollectionExtractor,
    "#exception": exception.HttpError,
},

{
    "#url"     : "https://www.fashionnova.com/collections/mini-dresses/?page=1",
    "#category": ("shopify", "fashionnova", "collection"),
    "#class"   : shopify.ShopifyCollectionExtractor,
},

{
    "#url"     : "https://www.fashionnova.com/collections/mini-dresses#1",
    "#category": ("shopify", "fashionnova", "collection"),
    "#class"   : shopify.ShopifyCollectionExtractor,
},

{
    "#url"     : "https://www.fashionnova.com/products/all-my-life-legging-black",
    "#category": ("shopify", "fashionnova", "product"),
    "#class"   : shopify.ShopifyProductExtractor,
    "#exception": exception.HttpError,
},

{
    "#url"     : "https://www.fashionnova.com/collections/flats/products/name",
    "#category": ("shopify", "fashionnova", "product"),
    "#class"   : shopify.ShopifyProductExtractor,
},

)
