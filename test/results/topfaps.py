# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import topfaps

__tests__ = (
{
    "#url"     : "https://topfaps.com/model/gabsthebunny",
    "#class"   : topfaps.TopfapsModelExtractor,
    "#pattern" : r"https://topfaps\.com/storage/images/22177/30341788/e69cfcf59292066076dff06098c27c85\.webp",
    "#count"   : 290,
},
{
    "#url"     : "https://topfaps.com/photo/30341788",
    "#class"   : topfaps.TopfapsPostExtractor,
    "#results" : "https://topfaps.com/storage/images/22177/30341788/e69cfcf59292066076dff06098c27c85.webp",
},

{
    "#url"     : "https://topfaps.com/video/6219897",
    "#class"   : topfaps.TopfapsPostExtractor,
    "#results" : "ytdl:https://topfaps.com/m3u8/6219897.m3u8?time=1793896954&sig=7501d56bc2d3c44ffd654ca58801f0fa366d493ae64db009eafefec58f2ca320&sig2=syV7PlszwUrbASGV",
},
)

