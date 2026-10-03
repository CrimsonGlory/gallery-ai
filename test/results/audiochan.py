# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import audiochan


__tests__ = (
{
    "#url"     : "https://audiochan.com/a/pBP1V1ODEV2od9CjLu",
    "#class"   : audiochan.AudiochanAudioExtractor,
    "#pattern" : r"https://stream\.audiochan\.com/(?:v\?token=.+|\?pt=.+)",
    "#count"   : 1,

    "description": [
        "author summary: ",
        "You wake up in the middle of the night, noticing that your boyfriend is still awake and restlessly moving around. Work-related worries are making him anxious and keeping him from falling asleep so you do your best to take care of him, calm him down, and help him get some rest."
    ],
    "user": {
        "username": "lil-lovergirl",
    },
},

{
    "#url"     : "https://audiochan.com/u/lil-lovergirl",
    "#class"   : audiochan.AudiochanUserExtractor,
    "#pattern" : r"https://stream\.audiochan\.com/(?:v\?token=.+|\?pt=.+)",
    "#count"   : range(35, 50),

    "user": {
        "username": "lil-lovergirl",
    },
},

{
    "#url"     : "https://audiochan.com/c/qzrByaXAwTLVXRgC9m",
    "#class"   : audiochan.AudiochanCollectionExtractor,
    "#pattern" : r"https://(?:content|stream)\.audiochan\.com/.+",
    "#count"   : range(5, 20),

    "collection": {
        "id": "6d7a89a4-e752-4772-923d-65783aee332e",
        "slug": "qzrByaXAwTLVXRgC9m",
        "title": "💗SFW",
    },
    "user": {
        "username": "lil-lovergirl",
    },
},

{
    "#url"     : "https://audiochan.com/search?q=Cozy&sort=trending&timeRange=all",
    "#class"   : audiochan.AudiochanSearchExtractor,
    "#count"   : range(15, 40),

    "search_tags": "Cozy",
    "description": list,
    "user": dict,
    "tags": list,
},

)
