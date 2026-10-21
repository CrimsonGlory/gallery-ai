# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import imgbox
from gallery_dl import exception


__tests__ = (
{
    "#url"     : "https://imgbox.com/g/JaX5V5HX7g",
    "#category": ("", "imgbox", "gallery"),
    "#class"   : imgbox.ImgboxGalleryExtractor,
    "#pattern" : r"https://images\d+\.imgbox\.com/[0-9a-f]{2}/[0-9a-f]{2}/\w+_o\.\w+",
    "#count"   : 2,

    "gallery_key": "JaX5V5HX7g",
    "title"      : 'test-テスト-"&>',
},

{
    "#url"     : "https://imgbox.com/g/cUGEkRbdZZ",
    "#category": ("", "imgbox", "gallery"),
    "#class"   : imgbox.ImgboxGalleryExtractor,
    "#pattern" : r"https://images\d+\.imgbox\.com/[0-9a-f]{2}/[0-9a-f]{2}/\w+_o\.\w+",
    "#count"   : range(5, 20),
},

{
    "#url"     : "https://imgbox.com/g/JaX5V5HX7h",
    "#category": ("", "imgbox", "gallery"),
    "#class"   : imgbox.ImgboxGalleryExtractor,
    "#exception": exception.NotFoundError,
},

{
    "#url"     : "https://imgbox.com/qHhw7lpG",
    "#category": ("", "imgbox", "image"),
    "#class"   : imgbox.ImgboxImageExtractor,
    "#results" : "https://images3.imgbox.com/6d/9a/qHhw7lpG_o.png",

    "extension": "png",
    "filename" : "qHhw7lpG_o",
    "image_key": "qHhw7lpG",
    "num"      : None,
},

{
    "#url"     : "https://imgbox.com/qHhw7lpH",
    "#category": ("", "imgbox", "image"),
    "#class"   : imgbox.ImgboxImageExtractor,
    "#exception": exception.NotFoundError,
},

{
    "#url"     : "https://images3.imgbox.com/6d/9a/qHhw7lpG_o.png",
    "#comment" : "direct link",
    "#class"   : imgbox.ImgboxImageExtractor,
    "#results" : "https://images3.imgbox.com/6d/9a/qHhw7lpG_o.png",

    "extension": "png",
    "filename" : "qHhw7lpG_o",
    "image_key": "qHhw7lpG",
    "num"      : None,
},

{
    "#url"     : "https://i.imgbox.com/ivEi0Dgm.jpg",
    "#comment" : "direct link",
    "#class"   : imgbox.ImgboxImageExtractor,
    "#results" : "https://images3.imgbox.com/72/e9/ivEi0Dgm_o.jpg",

    "extension": "jpg",
    "filename" : "ivEi0Dgm_o",
    "image_key": "ivEi0Dgm",
    "num"      : "1",
},

)
