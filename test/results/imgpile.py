# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import imgpile


__tests__ = (
{
    "#url"     : "https://imgpile.com/p/bbjiXrl",
    "#class"   : imgpile.ImgpilePostExtractor,
    "#results" : (
        "https://cdn.imgpile.com/f/BobTUou.jpg",
        "https://cdn.imgpile.com/f/Wr9cQFK.jpg",
        "https://cdn.imgpile.com/f/VevZbjw.png",
    ),

    "id"       : int,
    "id_slug"  : {"BobTUou", "Wr9cQFK", "VevZbjw"},
    "count"    : 3,
    "num"      : range(1, 3),
    "filename" : str,
    "extension": {"jpg", "png"},
    "url"      : r"re:https://cdn.imgpile.com/f/\w+\.(jpg|png)",
    "post"     : {
        "author" : "zilla_64",
        "count"  : 3,
        "id"     : int,
        "id_slug": "bbjiXrl",
        "score"  : int,
        "title"  : "Mecha-King Ghidorah scans",
        "views"  : int,
        "tags"   : list,
    },
},

{
    "#url"     : "https://imgpile.com/u/zilla_64",
    "#class"   : imgpile.ImgpileUserExtractor,
    "#pattern" : imgpile.ImgpilePostExtractor.pattern,
    "#count"   : 16,
},

)
