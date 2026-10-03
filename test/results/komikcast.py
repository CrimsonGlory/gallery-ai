# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import komikcast
from gallery_dl import exception


__tests__ = (
{
    "#url"     : "https://komikcast.li/chapter/apotheosis-chapter-02-2-bahasa-indonesia/",
    "#class"   : komikcast.KomikcastChapterExtractor,
    "#exception": exception.AbortExtraction,
},

{
    "#url"     : "https://komikcast02.com/chapter/apotheosis-chapter-02-2-bahasa-indonesia/",
    "#class"   : komikcast.KomikcastChapterExtractor,
    "#exception": exception.AbortExtraction,
},

{
    "#url"     : "https://komikcast.lol/chapter/apotheosis-chapter-02-2-bahasa-indonesia/",
    "#class"   : komikcast.KomikcastChapterExtractor,
    "#exception": exception.AbortExtraction,
},

{
    "#url"     : "https://komikcast.site/chapter/apotheosis-chapter-02-2-bahasa-indonesia/",
    "#class"   : komikcast.KomikcastChapterExtractor,
    "#exception": exception.AbortExtraction,
},

{
    "#url"     : "https://komikcast.me/chapter/apotheosis-chapter-02-2-bahasa-indonesia/",
    "#class"   : komikcast.KomikcastChapterExtractor,
    "#exception": exception.AbortExtraction,
},

{
    "#url"     : "https://komikcast.com/chapter/apotheosis-chapter-02-2-bahasa-indonesia/",
    "#class"   : komikcast.KomikcastChapterExtractor,
    "#exception": exception.AbortExtraction,
},

{
    "#url"     : "https://komikcast.cz/chapter/apotheosis-chapter-02-2-bahasa-indonesia/",
    "#class"   : komikcast.KomikcastChapterExtractor,
    "#exception": exception.AbortExtraction,
},

{
    "#url"     : "https://komikcast.la/chapter/apotheosis-chapter-02-2-bahasa-indonesia/",
    "#class"   : komikcast.KomikcastChapterExtractor,
    "#exception": exception.AbortExtraction,
},

{
    "#url"     : "https://komikcast.me/chapter/soul-land-ii-chapter-300-1-bahasa-indonesia/",
    "#class"   : komikcast.KomikcastChapterExtractor,
    "#exception": exception.AbortExtraction,
},

{
    "#url"     : "https://komikcast.site/komik/090-eko-to-issho/",
    "#class"   : komikcast.KomikcastMangaExtractor,
    "#exception": exception.AbortExtraction,
},

{
    "#url"     : "https://komikcast.me/tonari-no-kashiwagi-san/",
    "#class"   : komikcast.KomikcastMangaExtractor,
    "#exception": exception.AbortExtraction,
},

)
