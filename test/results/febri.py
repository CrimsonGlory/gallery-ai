# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import febri
from gallery_dl import exception


__tests__ = (
{
    "#url"      : "https://febri.jp/topics/series_naomi_payton_01-01/",
    "#comment"  : "site closed 2026-11-25",
    "#class"    : febri.FebriArticleExtractor,
    "#exception": exception.NotFoundError,
},

{
    "#url"      : "https://febri.jp/topics/",
    "#comment"  : "site closed 2026-11-25",
    "#class"    : febri.FebriTopicsExtractor,
    "#exception": exception.NotFoundError,
},

)
