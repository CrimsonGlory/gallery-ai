# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import imagehosts
from gallery_dl import exception


__tests__ = (
{
    "#url"     : "https://www.imagevenue.com/ME13LS07",
    "#category": ("imagehost", "imagevenue", "image"),
    "#class"   : imagehosts.ImagevenueImageExtractor,
    "#exception": exception.NotFoundError,

    "extension": "png",
    "filename" : "test-テスト-\"&>",
    "token"    : "ME13LS07",
},

{
    "#url"     : "https://www.imagevenue.com/view/o?i=92518_13732377annakarina424200712535AM_122_486lo.jpg&h=img150&l=loc486",
    "#category": ("imagehost", "imagevenue", "image"),
    "#class"   : imagehosts.ImagevenueImageExtractor,
    "#exception": exception.NotFoundError,
},

{
    "#url"     : "http://img28116.imagevenue.com/img.php?image=th_52709_test_122_64lo.jpg",
    "#category": ("imagehost", "imagevenue", "image"),
    "#class"   : imagehosts.ImagevenueImageExtractor,
    "#exception": exception.NotFoundError,
},

{
    "#url"     : "http://img159.imagevenue.com/img.php?image=73874_203_123_83lo.jpg",
    "#comment" : "404 image (#7570)",
    "#category": ("imagehost", "imagevenue", "image"),
    "#class"   : imagehosts.ImagevenueImageExtractor,
    "#exception": exception.NotFoundError,
},

{
    "#url"     : "http://img42.imagevenue.com/img.php?loc=loc1003%E2%84%91=20377_Alessandra_Ambrosio_Celebrity_City_Arriving_Mokai_Nightclub_17_13_1003lo.jpg",
    "#comment" : "dead link / '404 Image Unavailable' redirect (#8477)",
    "#category": ("imagehost", "imagevenue", "image"),
    "#class"   : imagehosts.ImagevenueImageExtractor,
    "#exception": exception.NotFoundError,
},

)
