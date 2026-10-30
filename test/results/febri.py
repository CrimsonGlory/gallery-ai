# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import febri


__tests__ = (
{
    "#url"     : "https://febri.jp/topics/series_naomi_payton_01-01/",
    "#class"   : febri.FebriArticleExtractor,
    "#results" : (
        "https://febri.jp/wp/wp-content/uploads/2023/06/H5A2005_2400.jpg",
        "https://febri.jp/wp/wp-content/uploads/2023/06/H5A1950_1280.jpg",
        "https://febri.jp/wp/wp-content/uploads/2023/06/H5A1914_1280.jpg",
        "https://febri.jp/wp/wp-content/uploads/2023/06/H5A1972_1280.jpg",
        "https://febri.jp/wp/wp-content/uploads/2023/06/H5A1999_1280.jpg",
        "https://febri.jp/wp/wp-content/uploads/2023/06/H5A2038_1280.jpg",
        "https://febri.jp/wp/wp-content/uploads/2023/06/H5A2054_1280.jpg",
    ),

    "count"      : 7,
    "date"       : "dt:2023-07-01 03:05:15",
    "description": "「変身ヒロイン」ものは「普通の女の子」の物語 ――ペイトンさんの20歳の誕生日に第1回目が公開され、この連載が",
    "extension"  : "jpg",
    "filename"   : str,
    "num"        : range(1, 7),
    "slug"       : "series_naomi_payton_01-01",
    "summary"    : "声優・ペイトン尚未がさまざまな「ヒロイン」に扮し、憧れや理想を追求するフォト＆インタビュー連載。記念すべき20歳の誕生日にスタートを迎えた第1回は「変身ヒロイン」がテーマ。となれば、もちろん話題になるのは、折に触れて思い入れを語ってきた、あの人気シリーズ。中でも「最推し」のキャラクターは――？",
    "title"      : "ペイトン尚未の「並行多元ヒロインズ」第1回 変身ヒロインに愛を込めて（前編）",
    "url"        : "https://febri.jp/topics/series_naomi_payton_01-01/",
    "tags"       : [
        "インタビュー_TOPICS",
        "プリキュア",
        "ペイトン尚未",
        "声優",
    ],
},

{
    "#url"     : "https://febri.jp/topics/",
    "#class"   : febri.FebriTopicsExtractor,
    "#pattern" : febri.FebriArticleExtractor.pattern,
    "#count"   : 866,
},

)
