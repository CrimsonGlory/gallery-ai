# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import shareimage
from gallery_dl import exception


__tests__ = (
{
    "#url"      : "https://www.share-image.com/340-amateur-set-young-girl-with-big-boobs",
    "#comment"  : "old gallery URL returns 410 Gone",
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
    "#url"      : "https://www.share-image.com/image/24-latina-beauty-topless-on-a-tropical-beach",
    "#comment"  : "previous /image/ URL is gone",
    "#class"    : shareimage.ShareimageGalleryExtractor,
    "#exception": exception.NotFoundError,
},

{
    "#url"     : "https://www.share-image.com/galleries/1-redhead-log-cabin-weekend",
    "#class"   : shareimage.ShareimageGalleryExtractor,
    "#pattern" : r"https://www\.share-image\.com/media/full/[0-9a-f]{2}/.+\.webp",
    "#count"   : range(1, 50),

    "gallery_id" : 1,
    "gallery_url": "https://www.share-image.com/galleries/1-redhead-log-cabin-weekend",
    "title"      : "Redhead's weekend in a log cabin",
    "extension"  : "webp",
},

{
    "#url"      : "https://www.share-image.com/image/97-redhead-in-a-log-cabin-smiling-in-a-chunky-wool-sweater-by-the-window",
    "#comment"  : "previous /image/ URL is gone",
    "#class"    : shareimage.ShareimageGalleryExtractor,
    "#exception": exception.NotFoundError,
},

{
    "#url"     : "https://www.share-image.com/image/135-redhead-in-a-log-cabin-smiling-in-a-chunky-wool-sweater-by-the-window",
    "#class"   : shareimage.ShareimageGalleryExtractor,
    "#results" : "https://www.share-image.com/media/full/8c/redhead-in-a-log-cabin-smiling-in-a-chunky-wool-sweater-by-the-window-8cf0294fd6.webp",

    "gallery_id" : 135,
    "gallery_url": "https://www.share-image.com/image/135-redhead-in-a-log-cabin-smiling-in-a-chunky-wool-sweater-by-the-window",
    "title"      : "Redhead in a log cabin – smiling in a chunky wool sweater by the window",
    "extension"  : "webp",
},

)
