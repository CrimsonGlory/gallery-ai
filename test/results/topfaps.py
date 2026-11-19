# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import topfaps


__tests__ = (
{
    "#url"     : "https://topfaps.com/model/gabsthebunny",
    "#class"   : topfaps.TopfapsModelExtractor,
    "#pattern" : r"https://topfaps\.com/storage/images/22177/\w+/\w+\.webp",
    "#range"   : "1-100",
    "#count"   : 100,
},

{
    "#url"     : "https://topfaps.com/photo/30341788",
    "#class"   : topfaps.TopfapsPostExtractor,
    "#results" : "https://topfaps.com/storage/images/22177/30341788/e69cfcf59292066076dff06098c27c85.webp",

    "creator"  : "gabsthebunny",
    "extension": "webp",
    "filename" : "e69cfcf59292066076dff06098c27c85",
    "id"       : 30341788,
    "title"    : "Abierta para recibir una rica verga que aguante esta coneja gorda",
    "type"     : "photo",
},

{
    "#url"     : "https://topfaps.com/video/6219897",
    "#class"   : topfaps.TopfapsPostExtractor,
    "#pattern" : r"ytdl:https://topfaps.com/m3u8/6219897.m3u8\?time=\d+&sig=\w+&sig2=\w+",

    "creator"  : "gabsthebunny",
    "extension": "mp4",
    "filename" : "6219897",
    "id"       : 6219897,
    "title"    : "Alguien quiere montar a esta culona cu nto crees que dure sac ndote la",
    "type"     : "video",
},

)
