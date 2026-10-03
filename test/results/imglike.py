# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import chevereto
from gallery_dl import exception


__tests__ = (
{
    "#url"     : "https://imglike.com/image/EMT-Skills-Verification-by-EMSA.Lx6dT",
    "#category": ("chevereto", "imglike", "file"),
    "#class"   : chevereto.CheveretoFileExtractor,
    "#exception": exception.HttpError,

    "album"    : "",
    "date"     : "dt:2022-08-12 06:36:10",
    "extension": "gif",
    "filename" : "EMT-Skills-Verification-by-EMSA",
    "id"       : "Lx6dT",
    "url"      : "https://imglike.com/images/2022/08/12/EMT-Skills-Verification-by-EMSA.gif",
    "user"     : "albertthomas9",
},

{
    "#url"     : "https://www.imglike.com/image/EMT-Skills-Verification-by-EMSA.Lx6dT",
    "#category": ("chevereto", "imglike", "file"),
    "#class"   : chevereto.CheveretoFileExtractor,
},

{
    "#url"     : "https://imglike.com/albertthomas9",
    "#category": ("chevereto", "imglike", "user"),
    "#class"   : chevereto.CheveretoUserExtractor,
    "#exception": exception.HttpError,
},

{
    "#url"     : "https://imglike.com/album/Kara-Del-Toro-Naked.cG7l",
    "#category": ("chevereto", "imglike", "album"),
    "#class"   : chevereto.CheveretoAlbumExtractor,
    "#exception": exception.HttpError,
},

{
    "#url"     : "https://imglike.com/category/Bursting-boobs",
    "#category": ("chevereto", "imglike", "category"),
    "#class"   : chevereto.CheveretoCategoryExtractor,
    "#exception": exception.HttpError,
},

)
