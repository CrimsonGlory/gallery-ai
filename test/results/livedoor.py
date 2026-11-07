# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import livedoor


__tests__ = (
{
    "#url"     : "http://blog.livedoor.jp/zatsu_ke/",
    "#category": ("", "livedoor", "blog"),
    "#class"   : livedoor.LivedoorBlogExtractor,
    "#pattern" : r"https?://livedoor.blogimg.jp/\w+/imgs/\w/\w/\w+\.\w+",
    "#range"   : "1-50",
    "#count"   : 50,
    "#archive" : False,

    "post"    : {
        "categories" : tuple,
        "date"       : "type:datetime",
        "description": str,
        "id"         : int,
        "tags"       : list,
        "title"      : str,
        "user"       : "zatsu_ke",
    },
    "filename": str,
    "hash"    : r"re:\w{4,}",
    "num"     : int,
},

{
    "#url"     : "http://blog.livedoor.jp/uotapo/",
    "#category": ("", "livedoor", "blog"),
    "#class"   : livedoor.LivedoorBlogExtractor,
    "#range"   : "1-5",
    "#count"   : 5,
},

{
    "#url"     : "http://blog.livedoor.jp/maosorakazu/",
    "#comment" : "'blog.livedoor.jp' -> 'maosorakazu.livedoor.blog' redirect",
    "#class"   : livedoor.LivedoorBlogExtractor,
    "#range"   : "1-5",
    "#results" : (
        "https://livedoor.blogimg.jp/maosorakazu/imgs/c/c/cc3765e6.jpg",
        "https://livedoor.blogimg.jp/maosorakazu/imgs/d/a/daef6121.jpg",
        "https://livedoor.blogimg.jp/maosorakazu/imgs/2/a/2ae36986.jpg",
        "https://livedoor.blogimg.jp/maosorakazu/imgs/9/b/9b947aae.jpg",
        "https://livedoor.blogimg.jp/maosorakazu/imgs/6/6/66cfc3d2.jpg",
    ),

    "post"     : {
        "date"       : "type:datetime",
        "tags"       : [],
        "user"       : "maosorakazu",
    },
},

{
    "#url"     : "https://maosorakazu.livedoor.blog/",
    "#comment" : "'USER.livedoor.blog' URL",
    "#class"   : livedoor.LivedoorBlogExtractor,
    "#range"   : "1-5",
    "#results" : (
        "https://livedoor.blogimg.jp/maosorakazu/imgs/c/c/cc3765e6.jpg",
        "https://livedoor.blogimg.jp/maosorakazu/imgs/d/a/daef6121.jpg",
        "https://livedoor.blogimg.jp/maosorakazu/imgs/2/a/2ae36986.jpg",
        "https://livedoor.blogimg.jp/maosorakazu/imgs/9/b/9b947aae.jpg",
        "https://livedoor.blogimg.jp/maosorakazu/imgs/6/6/66cfc3d2.jpg",
    ),

    "post"     : {
        "date"       : "type:datetime",
        "tags"       : [],
        "user"       : "maosorakazu",
    },
},

{
    "#url"     : "http://blog.livedoor.jp/zatsu_ke/archives/51493859.html",
    "#category": ("", "livedoor", "post"),
    "#class"   : livedoor.LivedoorPostExtractor,
    "#sha1_url"     : "9ca3bbba62722c8155be79ad7fc47be409e4a7a2",
    "#sha1_metadata": "1f5b558492e0734f638b760f70bfc0b65c5a97b9",
},

{
    "#url"     : "http://blog.livedoor.jp/amaumauma/archives/7835811.html",
    "#class"   : livedoor.LivedoorPostExtractor,
    "#results" : (
        "https://livedoor.blogimg.jp/amaumauma/imgs/9/5/95b3cb6b.jpg",
        "https://livedoor.blogimg.jp/amaumauma/imgs/4/5/4517d3f8.jpg",
        "https://livedoor.blogimg.jp/amaumauma/imgs/6/2/625c6907.gif",
    ),

    "post"     : {
        "categories" : ("", ""),
        "date"       : "dt:2015-03-10 07:05:11",
        "description": "どうもとってもお久しぶりです。甘兎です。かなり、かな～り期間が空いてしまいました･･･大丈夫です。生きてます。最近はちょくちょくお仕事ももらえる様になり嬉しい限りです！仕事の合間を縫って色々やってたらブログのことすっかり忘れておりました。申し訳ない！！ソーシ",
        "id"         : 7835811,
        "tags"       : [],
        "title"      : "生存報告",
        "user"       : "amaumauma",
    },
},

{
    "#url"     : "http://blog.livedoor.jp/uotapo/archives/1050616939.html",
    "#class"   : livedoor.LivedoorPostExtractor,
    "#results" : (
        "https://livedoor.blogimg.jp/uotapo/imgs/f/e/fe1ee67c.jpg",
        "https://livedoor.blogimg.jp/uotapo/imgs/1/2/12e44c76.jpg",
    ),

    "post"     : {
        "categories" : ("マイリトルポニー", "Equestria Girls"),
        "date"       : "dt:2016-01-24 13:29:44",
        "description": "ポニーレスになって早２ヶ月が経とうとしていますが、エクエストリアガールズ好きとしては、シマーレスから４ヶ月になる事も問題です。だもんで、勝手に次回作の内容を想像（妄想）してみたいと思います。",
        "id"         : 1050616939,
        "tags"       : ["#mylittlepony"],
        "title"      : "エクエストリアガールズ４を予想してみる",
        "user"       : "uotapo",
    },
},

{
    "#url"     : "http://blog.livedoor.jp/maosorakazu/archives/1409825.html",
    "#comment" : "'blog.livedoor.jp' -> 'maosorakazu.livedoor.blog' redirect",
    "#class"   : livedoor.LivedoorPostExtractor,
    "#results" : "https://livedoor.blogimg.jp/maosorakazu/imgs/6/2/62f20ac2.jpg",

    "post"     : {
        "categories" : ("", ""),
        "date"       : "dt:2019-08-07 15:00:11",
        "description": "私の人生は大ハズレだ。 おみくじで言えば大凶。色で言えば真っ黒。 たった十二年間しか生きてないのに何がわかると思われるかもしれないが、逆に言ってしまえば十二年間も同じ景色の人生なんだ。明るい色が入ってくることはないだろう。 きっと後七十年間近くは同じよ",
        "id"         : 1409825,
        "tags"       : [],
        "title"      : "小説「猫の音」（第一回）",
        "user"       : "maosorakazu",
    },
},

{
    "#url"     : "https://maosorakazu.livedoor.blog/archives/1409825.html",
    "#comment" : "'USER.livedoor.blog' URL",
    "#class"   : livedoor.LivedoorPostExtractor,
    "#results" : "https://livedoor.blogimg.jp/maosorakazu/imgs/6/2/62f20ac2.jpg",

    "extension": "jpg",
    "filename" : "イラスト144",
    "hash"     : "62f20ac2",
    "num"      : 1,
    "url"      : "https://livedoor.blogimg.jp/maosorakazu/imgs/6/2/62f20ac2.jpg",
    "post"     : {
        "categories" : ("", ""),
        "date"       : "dt:2019-08-07 15:00:11",
        "description": "私の人生は大ハズレだ。 おみくじで言えば大凶。色で言えば真っ黒。 たった十二年間しか生きてないのに何がわかると思われるかもしれないが、逆に言ってしまえば十二年間も同じ景色の人生なんだ。明るい色が入ってくることはないだろう。 きっと後七十年間近くは同じよ",
        "id"         : 1409825,
        "tags"       : [],
        "title"      : "小説「猫の音」（第一回）",
        "user"       : "maosorakazu",
    },
},

)
