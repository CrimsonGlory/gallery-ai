# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import imagebam


__tests__ = (
{
    "#url"     : "https://www.imagebam.com/gallery/adz2y0f9574bjpmonaismyrhtjgvey4o",
    "#class"   : imagebam.ImagebamGalleryExtractor,
    "#pattern" : r"https://images\d+\.imagebam\.com/[A-Za-z0-9_./-]+\.(?:jpe?g|png|gif|webp)",
    "#count"   : 2,
},

{
    "#url"     : "http://www.imagebam.com/gallery/op9dwcklwdrrguibnkoe7jxgvig30o5p",
    "#class"   : imagebam.ImagebamGalleryExtractor,
    "#pattern" : r"https://images\d+\.imagebam\.com/[A-Za-z0-9_./-]+\.(?:jpe?g|png|gif|webp)",
    "#range"   : "1-50",
    "#count"   : range(1, 51),
},

{
    "#url"     : "http://www.imagebam.com/gallery/gsl8teckymt4vbvx1stjkyk37j70va2c",
    "#comment" : "'The page could not be found'",
    "#class"   : imagebam.ImagebamGalleryExtractor,
    "#exception": "NotFoundError",
},

{
    "#url"     : "https://www.imagebam.com/view/GA3MT1",
    "#comment" : "/view/ path (#2378)",
    "#class"   : imagebam.ImagebamGalleryExtractor,
    "#pattern" : r"https://images\d+\.imagebam\.com/[A-Za-z0-9_./-]+\.(?:jpe?g|png|gif|webp)",
    "#count"   : range(1, 20),
},

{
    "#url"     : "https://www.imagebam.com/image/94d56c502511890",
    "#class"   : imagebam.ImagebamImageExtractor,
    "#results" : "https://images3.imagebam.com/1d/8c/44/94d56c502511890.png",

    "extension": "png",
    "filename" : 'test-???-"&>',
    "image_key": "94d56c502511890",
    "url"      : "https://images3.imagebam.com/1d/8c/44/94d56c502511890.png",
},

{
    "#url"     : "http://images3.imagebam.com/1d/8c/44/94d56c502511890.png",
    "#class"   : imagebam.ImagebamImageExtractor,
},

{
    "#url"     : "https://www.imagebam.com/image/0850951366904951",
    "#comment" : "NSFW (#1534)",
    "#class"   : imagebam.ImagebamImageExtractor,
    "#results" : "https://images2.imagebam.com/ac/83/68/0850951366904951.jpg",

    "extension": "jpg",
    "filename" : "5884006",
    "image_key": "0850951366904951",
    "url"      : "https://images2.imagebam.com/ac/83/68/0850951366904951.jpg",
},

{
    "#url"     : "https://www.imagebam.com/view/ME8JOQP",
    "#comment" : "/view/ path (#2378)",
    "#class"   : imagebam.ImagebamImageExtractor,
    "#exception": "NotFoundError",
},

{
    "#url"     : "https://www.imagebam.com/image/b728aa119132443",
    "#comment" : "filename without extension (#8476)",
    "#class"   : imagebam.ImagebamImageExtractor,
    "#results" : "https://images3.imagebam.com/d2/7a/d9/b728aa119132443.jpg",

    "extension": "",
    "filename" : "34415_AlessandraAmbrosio_PhotoshootforVictoriasSecretwearingbikinislingerieonthebeachinMalibuCalifor",
    "image_key": "b728aa119132443",
    "url"      : "https://images3.imagebam.com/d2/7a/d9/b728aa119132443.jpg",
},

{
    "#url"      : "https://www.imagebam.com/image/40a481151474621",
    "#comment"  : "deleted image (#8890)",
    "#class"    : imagebam.ImagebamImageExtractor,
    "#exception": "NotFoundError",
},

)
