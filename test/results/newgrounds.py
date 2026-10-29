# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import newgrounds


__tests__ = (
{
    "#url"     : "https://www.newgrounds.com/art/view/tomfulp/ryu-is-hawt",
    "#category": ("", "newgrounds", "image"),
    "#class"   : newgrounds.NewgroundsImageExtractor,
    "#pattern"     : r"https://art\.ngfiles\.com/images/1993000/1993615_4474_tomfulp_ryu-is-hawt\.[0-9a-f]+\.(?:gif|webp)\?f\d+",

    "artist"     : ["tomfulp"],
    "comment"    : str,
    "date"       : "dt:2009-06-04 14:44:05",
    "description": "",
    "favorites"  : int,
    "filename"   : str,
    "height"     : 476,
    "index"      : 1993615,
    "rating"     : "e",
    "score"      : float,
    "slug"       : "ryu-is-hawt",
    "tags"       : [
        "ryu",
        "streetfighter",
    ],
    "title"      : "Ryu is Hawt",
    "type"       : "art",
    "user"       : "tomfulp",
    "width"      : 447,
},

{
    "#url"     : "https://art.ngfiles.com/images/0/94_tomfulp_ryu-is-hawt.gif",
    "#category": ("", "newgrounds", "image"),
    "#class"   : newgrounds.NewgroundsImageExtractor,
    "#pattern" : r"https://art\.ngfiles\.com/images/1993000/1993615_4474_tomfulp_ryu-is-hawt\.[0-9a-f]+\.(?:gif|webp)\?f\d+",

    "slug" : "ryu-is-hawt",
    "title": "Ryu is Hawt",
},

{
    "#url"     : "https://www.newgrounds.com/art/view/sailoryon/yon-dream-buster",
    "#comment" : "embedded file in 'comments' (#1033)",
    "#category": ("", "newgrounds", "image"),
    "#class"   : newgrounds.NewgroundsImageExtractor,
    "#results" : (
        "https://art.ngfiles.com/images/1438000/1438673_sailoryon_yon-dream-buster.jpg?f1601058173",
        "https://art.ngfiles.com/comments/172000/iu_172374_7112211.jpg",
    ),

    "slug" : "yon-dream-buster",
    "title": "Yon Dream Buster!",
},

{
    "#url"     : "https://www.newgrounds.com/art/view/zedrinbot/lewd-animation-tutorial",
    "#comment" : "extra files in 'art-image-row' elements - WebP to GIF (#4642)",
    "#category": ("", "newgrounds", "image"),
    "#class"   : newgrounds.NewgroundsImageExtractor,
    "#auth"    : True,
    "#results" : (
        "https://art.ngfiles.com/images/5091000/5091275_45067_zedrinbot_untitled-5091275.0a9d27ed2bc265a7e89478ed6ad6f86f.gif?f1696187399",
        "https://art.ngfiles.com/images/5091000/5091275_45071_zedrinbot_untitled-5091275.6fdc62eaef43528fb1c9bda624d30a3d.gif?f1696187436",
        "https://art.ngfiles.com/images/5091000/5091275_45070_zedrinbot_untitled-5091275.0d7334746374465bd448908b88d1f810.gif?f1696187434",
        "https://art.ngfiles.com/images/5091000/5091275_45072_zedrinbot_untitled-5091275.6fdc62eaef43528fb1c9bda624d30a3d.gif?f1696187437",
        "https://art.ngfiles.com/images/5091000/5091275_45073_zedrinbot_untitled-5091275.20aa05c1cd22fd058e8c68ce58f5a302.gif?f1696187437",
    ),
},

{
    "#url"     : "https://www.newgrounds.com/art/view/zedrinbot/nazrin-tanlines",
    "#comment" : "extra files in 'art-image-row' elements - native PNG files (#4642)",
    "#category": ("", "newgrounds", "image"),
    "#class"   : newgrounds.NewgroundsImageExtractor,
    "#auth"    : True,
    "#results" : (
        "https://art.ngfiles.com/images/5009000/5009916_14628_zedrinbot_nazrin-tanlines.265f7b6beec5855a349e2646e90cbc01.png?f1695698131",
        "https://art.ngfiles.com/images/5009000/5009916_14632_zedrinbot_nazrin-tanlines.40bd62fbf5875806cda6b004b348114a.png?f1695727318",
        "https://art.ngfiles.com/images/5009000/5009916_14634_zedrinbot_nazrin-tanlines.40bd62fbf5875806cda6b004b348114a.png?f1695727321",
        "https://art.ngfiles.com/images/5009000/5009916_14633_zedrinbot_nazrin-tanlines.40bd62fbf5875806cda6b004b348114a.png?f1695727318",
        "https://art.ngfiles.com/images/5009000/5009916_14635_zedrinbot_nazrin-tanlines.6a7aa4fd63e5f8077ad29314568246cc.png?f1695727321",
        "https://art.ngfiles.com/images/5009000/5009916_14636_zedrinbot_nazrin-tanlines.6a7aa4fd63e5f8077ad29314568246cc.png?f1695727322",
    ),
},

{
    "#url"     : "https://www.newgrounds.com/art/view/bacun/kill-la-kill-10th-anniversary",
    "#comment" : "extra files in 'imageData' block (#4642)",
    "#category": ("", "newgrounds", "image"),
    "#class"   : newgrounds.NewgroundsImageExtractor,
    "#results" : (
        "https://art.ngfiles.com/images/5127000/5127150_93307_bacun_kill-la-kill-10th-anniversary.61adfe309bec342f9db55fd44397235b.png?f1697310027",
        "https://art.ngfiles.com/images/5127000/5127150_94250_bacun_kill-la-kill-10th-anniversary.64fdf525fa38c1ab34defac4b354bc7a.png?f1697332147",
    ),
},

{
    "#url"     : "https://www.newgrounds.com/art/view/sockdotclip/trickin-treats",
    "#comment" : "extra files in comment section as '<img src=' (#6253)",
    "#class"   : newgrounds.NewgroundsImageExtractor,
    "#results" : (
        "https://art.ngfiles.com/images/2811000/2811344_sockdotclip_trickin-treats.png?f1667246310",
        "https://art.ngfiles.com/comments/788000/iu_788899_10504416.webp",
        "https://art.ngfiles.com/comments/788000/iu_788901_10504416.webp",
        "https://art.ngfiles.com/comments/788000/iu_788900_10504416.webp",
        "https://art.ngfiles.com/comments/788000/iu_788903_10504416.webp",
        "https://art.ngfiles.com/comments/788000/iu_788902_10504416.webp",
    ),
},

{
    "#url"     : "https://www.newgrounds.com/art/view/kekiiro/red",
    "#comment" : "'adult' rated (#2456)",
    "#category": ("", "newgrounds", "image"),
    "#class"   : newgrounds.NewgroundsImageExtractor,
    "#options" : {"username": None},
    "#count"   : 0,
},

{
    "#url"     : "https://www.newgrounds.com/art/view/shamfoo/arigatou-ke-xue-zhe69",
    "#comment" : "japanese title, ascii slug (#8064)",
    "#class"   : newgrounds.NewgroundsImageExtractor,
    "#results" : "https://art.ngfiles.com/images/878000/878868_shamfoo_arigatou-ke-xue-zhe69.png?f1555537672",

    "slug" : "arigatou-ke-xue-zhe69",
    "title": "ありがとう科学者69",
},

{
    "#url"     : "https://www.newgrounds.com/portal/view/595355",
    "#comment" : "video",
    "#category": ("", "newgrounds", "media"),
    "#class"   : newgrounds.NewgroundsMediaExtractor,
    "#results" : "https://uploads.ungrounded.net/alternate/564000/564957_alternate_31.mp4?1359712249",

    "artist"     : [
        "kickinthehead",
        "danpaladin",
        "tomfulp",
    ],
    "comment"    : r"re:My fan trailer for Alien Hominid HD!",
    "date"       : "dt:2013-02-01 09:50:49",
    "description": "Fan trailer for Alien Hominid HD!",
    "favorites"  : int,
    "filename"   : "564957_alternate_31",
    "index"      : 595355,
    "rating"     : "e",
    "score"      : float,
    "tags"       : [
        "alienhominid",
        "trailer",
    ],
    "title"      : "Alien Hominid Fan Trailer",
    "type"       : "movie",
    "user"       : "kickinthehead",
},

{
    "#url"     : "https://www.newgrounds.com/portal/view/595355",
    "#category": ("", "newgrounds", "media"),
    "#class"   : newgrounds.NewgroundsMediaExtractor,
    "#options" : {"format": ["mkv", "mov", 1080]},
    "#results" : "https://uploads.ungrounded.net/alternate/564000/564957_alternate_31.mkv?1359712249",
},

{
    "#url"     : "https://www.newgrounds.com/portal/view/595355",
    "#category": ("", "newgrounds", "media"),
    "#class"   : newgrounds.NewgroundsMediaExtractor,
    "#options" : {"format": "720p"},
    "#results" : "https://uploads.ungrounded.net/alternate/564000/564957_alternate_31.720p.mp4?1359712249",
},

{
    "#url"     : "https://www.newgrounds.com/audio/listen/609768",
    "#comment" : "audio",
    "#category": ("", "newgrounds", "media"),
    "#class"   : newgrounds.NewgroundsMediaExtractor,
    "#sha1_url": "f4c5490ae559a3b05e46821bb7ee834f93a43c95",

    "artist"     : [
        "zj",
        "tomfulp",
    ],
    "comment"    : str,
    "date"       : "dt:2015-02-23 19:31:59",
    "description": "From The ZJ Report Show!",
    "favorites"  : int,
    "index"      : 609768,
    "rating"     : "",
    "score"      : float,
    "tags"       : [
        "fulp",
        "interview",
        "tom",
        "zj",
    ],
    "title"      : "ZJ Interviews Tom Fulp!",
    "type"       : "audio",
    "user"       : "zj",
},

{
    "#url"     : "https://www.newgrounds.com/portal/view/161181/format/flash",
    "#comment" : "flash animation (#1257)",
    "#category": ("", "newgrounds", "media"),
    "#class"   : newgrounds.NewgroundsMediaExtractor,
    "#pattern" : r"https://uploads\.ungrounded\.net/161000/161181_ddautta_mask__550x281_\.swf(?:\?.*)?",

    "type": {"movie", "game"},
},

{
    "#url"     : "https://www.newgrounds.com/portal/view/758545",
    "#comment" : "video format selection (#1729)",
    "#category": ("", "newgrounds", "media"),
    "#class"   : newgrounds.NewgroundsMediaExtractor,
    "#options" : {"format": "720p"},
    "#pattern" : r"https://uploads\.ungrounded\.net/alternate/1482000/1482860_alternate_102516\.720p\.mp4\?\d+",
},

{
    "#url"     : "https://www.newgrounds.com/portal/view/717744",
    "#comment" : "'adult' rated (#2456)",
    "#category": ("", "newgrounds", "media"),
    "#class"   : newgrounds.NewgroundsMediaExtractor,
    "#options" : {"username": None},
    "#count"   : range(0, 2),
},

{
    "#url"     : "https://www.newgrounds.com/portal/view/829032",
    "#comment" : "flash game",
    "#category": ("", "newgrounds", "media"),
    "#class"   : newgrounds.NewgroundsMediaExtractor,
    "#pattern" : r"https://uploads\.ungrounded\.net/(829000/829032_picovsbeardx\.swf|tmp/img/\d+/iu_\d+_\d+\.gif)(?:\?.*)?",
    "#count"   : range(2, 5),

    "artist"     : list,
    "comment"    : r"re:The children are expendable. Take out the ",
    "description": str,
    "favorites"  : int,
    "index"      : 829032,
    "post_url"   : "https://www.newgrounds.com/portal/view/829032",
    "rating"     : str,
    "score"      : float,
    "tags"       : list,
    "title"      : "PICO VS BEAR DX",
    "type"       : "game",
    "url"        : r"re:https://uploads\.ungrounded\.net/829000/829032_picovsbeardx\.swf(?:\?.*)?",
},

{
    "#url"     : "https://tomfulp.newgrounds.com/art",
    "#class"   : newgrounds.NewgroundsArtExtractor,
    "#pattern" : r"https://((?:art|img)\.ngfiles\.com/|uploads\.ungrounded\.net/tmp/img/)",
    "#count"   : ">= 3",
},

{
    "#url"     : "https://tomfulp.newgrounds.com/art/page/3",
    "#class"   : newgrounds.NewgroundsArtExtractor,
},

{
    "#url"     : "https://tomfulp.newgrounds.com/art?page=3",
    "#class"   : newgrounds.NewgroundsArtExtractor,
},

{
    "#url"     : "https://tomfulp.newgrounds.com/audio",
    "#class"   : newgrounds.NewgroundsAudioExtractor,
    "#pattern" : r"https://(audio\.ngfiles\.com/\d+/\d+_.+\.mp3|uploads\.ungrounded\.net/.+\.png|img\.ngfiles\.com/.+)",
    "#count"   : ">= 10",
},

{
    "#url"     : "https://tomfulp.newgrounds.com/audio?page=3",
    "#class"   : newgrounds.NewgroundsAudioExtractor,
},

{
    "#url"     : "https://tomfulp.newgrounds.com/movies",
    "#class"   : newgrounds.NewgroundsMoviesExtractor,
    "#pattern" : r"https://(uploads\.ungrounded\.net(/alternate)?/\d+/\d+_.+|img\.ngfiles\.com/.+)",
    "#range"   : "1-10",
    "#count"   : 10,
},

{
    "#url"     : "https://tomfulp.newgrounds.com/movies/?page=3",
    "#class"   : newgrounds.NewgroundsMoviesExtractor,
},

{
    "#url"     : "https://tomfulp.newgrounds.com/games",
    "#class"   : newgrounds.NewgroundsGamesExtractor,
    "#pattern" : r"https://(uploads.ungrounded.net(/alternate)?/(\d+/\d+_.+|tmp/.+)|img.ngfiles.com/)",
    "#range"   : "1-10",
    "#count"   : 10,

    "type": {"archive", "game"},
},

{
    "#url"     : "https://tomfulp.newgrounds.com/games?page=3",
    "#class"   : newgrounds.NewgroundsGamesExtractor,
},

{
    "#url"     : "https://tomfulp.newgrounds.com",
    "#class"   : newgrounds.NewgroundsUserExtractor,
    "#results" : "https://tomfulp.newgrounds.com/art",
},

{
    "#url"     : "https://tomfulp.newgrounds.com",
    "#class"   : newgrounds.NewgroundsUserExtractor,
    "#options" : {"include": "all"},
    "#results" : (
        "https://tomfulp.newgrounds.com/art",
        "https://tomfulp.newgrounds.com/audio",
        "https://tomfulp.newgrounds.com/games",
        "https://tomfulp.newgrounds.com/movies",
    ),
},

{
    "#url"     : "https://tomfulp.newgrounds.com/favorites/art",
    "#class"   : newgrounds.NewgroundsFavoriteExtractor,
    "#range"   : "1-10",
    "#count"   : ">= 10",
},

{
    "#url"     : "https://tomfulp.newgrounds.com/favorites/art?page=3",
    "#class"   : newgrounds.NewgroundsFavoriteExtractor,
},

{
    "#url"     : "https://tomfulp.newgrounds.com/favorites/audio",
    "#class"   : newgrounds.NewgroundsFavoriteExtractor,
},

{
    "#url"     : "https://tomfulp.newgrounds.com/favorites/movies",
    "#class"   : newgrounds.NewgroundsFavoriteExtractor,
},

{
    "#url"     : "https://tomfulp.newgrounds.com/favorites/",
    "#class"   : newgrounds.NewgroundsFavoriteExtractor,
},

{
    "#url"     : "https://tomfulp.newgrounds.com/favorites/following",
    "#class"   : newgrounds.NewgroundsFollowingExtractor,
    "#pattern" : newgrounds.NewgroundsUserExtractor.pattern,
    "#range"   : "76-125",
    "#count"   : 50,
},

{
    "#url"     : "https://tomfulp.newgrounds.com/favorites/following?page=3",
    "#class"   : newgrounds.NewgroundsFollowingExtractor,
},


{
    "#url"     : "https://www.newgrounds.com/search/conduct/art?terms=tree",
    "#class"   : newgrounds.NewgroundsSearchExtractor,
    "#pattern" : newgrounds.NewgroundsImageExtractor.pattern,
    "#range"   : "1-10",
    "#count"   : 10,

    "search_tags": "tree",
},

{
    "#url"     : "https://www.newgrounds.com/search/conduct/movies?terms=tree",
    "#class"   : newgrounds.NewgroundsSearchExtractor,
    "#pattern" : r"https://uploads.ungrounded.net(/alternate)?/\d+/\d+",
    "#range"   : "1-10",
    "#count"   : 10,
},

{
    "#url"     : "https://www.newgrounds.com/search/conduct/audio?advanced=1&terms=tree+green+nature&match=tdtu&genre=5&suitabilities=e%2Cm",
    "#class"   : newgrounds.NewgroundsSearchExtractor,
},

)
