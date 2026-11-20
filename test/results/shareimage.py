# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import shareimage
from gallery_dl import exception


__tests__ = (
{
    "#url"      : "https://www.share-image.com/340-amateur-set-young-girl-with-big-boobs",
    "#comment"  : "old gallery URL redirected after site redesign",
    "#class"    : shareimage.ShareimageGalleryExtractor,
    "#exception": exception.NotFoundError,
},

{
    "#url"      : "https://www.share-image.com/22836-cute-blonde-amateur-babe-shows-her-naked-body",
    "#comment"  : "old gallery URL redirected after site redesign",
    "#class"    : shareimage.ShareimageGalleryExtractor,
    "#exception": exception.NotFoundError,
},

{
    "#url"     : "https://www.share-image.com/image/24-latina-beauty-topless-on-a-tropical-beach",
    "#class"   : shareimage.ShareimageGalleryExtractor,
    "#results" : "https://www.share-image.com/media/full/fa/latina-beauty-topless-on-a-tropical-beach-fa72447466.webp",

    "gallery_id" : 24,
    "gallery_url": "https://www.share-image.com/image/24-latina-beauty-topless-on-a-tropical-beach",
    "title"      : "Latina beauty topless on a tropical beach",
    "extension"  : "webp",
},

)
