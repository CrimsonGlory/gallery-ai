# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import shimmie2


__tests__ = (
{
    "#url"     : "https://www.bittersweetcandybowl.com/candybooru/post/view/17985",
    "#category": ("shimmie2", "candybooru", "post"),
    "#class"   : shimmie2.Shimmie2PostExtractor,
    "#results" : "https://blasto.enterprises/candybooru/_images/ddb0f143b9f131f2fa80842d9a171148/17985%20-%20Abbey%20Amaya%20AnonFelis_%28Artist%29%20Augustus%20Daisy%20David%20excellent%20human%20Jasmine%20Jessica%20Lucy%20Madison%20Matt%20Mike%20Molly%20Paulo%20Rachel%20Sue%20Tess.png",

    "extension": "png",
    "file_url" : "https://blasto.enterprises/candybooru/_images/ddb0f143b9f131f2fa80842d9a171148/17985%20-%20Abbey%20Amaya%20AnonFelis_%28Artist%29%20Augustus%20Daisy%20David%20excellent%20human%20Jasmine%20Jessica%20Lucy%20Madison%20Matt%20Mike%20Molly%20Paulo%20Rachel%20Sue%20Tess.png",
    "filename" : "17985 - Abbey Amaya AnonFelis_(Artist) Augustus Daisy David excellent human Jasmine Jessica Lucy Madison Matt Mike Molly Paulo Rachel Sue Tess",
    "height"   : 2979,
    "id"       : 17985,
    "md5"      : "4a1ec1f5275c0c32e2922f4366667d71",
    "parent_id": None,
    "rating"   : "",
    "size"     : 0,
    "source"   : "",
    "tags"     : "256px; --thumb-height: 256px;}",
    "width"    : 3000,
},

{
    "#url"     : "https://www.bittersweetcandybowl.com/candybooru/post/list/JessicaxMadison/1",
    "#category": ("shimmie2", "candybooru", "tag"),
    "#class"   : shimmie2.Shimmie2TagExtractor,
    "#pattern" : r"https://www\.bittersweetcandybowl\.com/candybooru/_images/[0-9a-f]+",
    "#count"   : range(48, 80),

    "extension"  : str,
    "file_url"   : str,
    "filename"   : str,
    "height"     : 0,
    "id"         : int,
    "md5"        : "hash:md5",
    "search_tags": "JessicaxMadison",
    "size"       : 0,
    "tags"       : str,
    "width"      : 0,
},

)
