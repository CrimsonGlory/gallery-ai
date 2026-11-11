# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import tw6


__tests__ = (
{
    "#url"     : "https://tw6.jp/gallery/master/?master_id=4199",
    "#class"   : tw6.Tw6UserExtractor,
    "#pattern" : r"https://cdn\.tw6\.jp/i/tw6/(basic|thumb_grid)/\d+/\d+_\w+\.(jpg|png)",
    "#count"   : range(170, 300),

    "category_id"     : {1, 2, 4, 5, 9, 19, 22, 24, 30},
    "character_id"    : list,
    "character_name"  : str,
    "extension"       : {"jpg", "png"},
    "filename"        : str,
    "gallery_image_id": int,
    "heart_flag"      : False,
    "illust_id"       : int,
    "illust_title"    : str,
    "image_url"       : str,
    "is_portrait"     : bool,
    "is_voice"        : bool,
    "main_character_id": str,
    "master_id"       : "4199",
    "master_name"     : "かじゃねこ",
    "product"         : {"totalbody", "ic", "item_ic", "bu", "model_sheet", "rival_illust", "pinup", "battlepinup", "other"},
    "purchase_status" : 0,
    "purchase_text"   : "",
    "type"            : "illust",
},

{
    "#url"     : "https://tw6.jp/gallery/?id=210105",
    "#class"   : tw6.Tw6PostExtractor,
    "#results" : "https://cdn.tw6.jp/i/tw6/basic/2353/1324082_f23530_totalbody.jpg",

    "category_id"     : 4,
    "character_id"    : ["f23530"],
    "character_name"  : "ルメリー・マレフィカールム",
    "extension"       : "jpg",
    "filename"        : "1324082_f23530_totalbody",
    "gallery_image_id": 210105,
    "heart_flag"      : False,
    "illust_id"       : 210105,
    "illust_title"    : "",
    "image_url"       : "https://cdn.tw6.jp/i/tw6/basic/2353/1324082_f23530_totalbody.jpg",
    "is_portrait"     : True,
    "is_voice"        : False,
    "main_character_id": "f23530",
    "master_name"     : "かじゃねこ",
    "product"         : "totalbody",
    "purchase_status" : 0,
    "purchase_text"   : "",
    "type"            : "illust",
},

{
    "#url"     : "https://tw6.jp/gallery/search?word=%E3%81%8B%E3%81%98%E3%82%83%E3%81%AD%E3%81%93&sort=0&goods=0&min=10&max=0&sex=0&race=0&main_job=0&sub_job=0&condition=0&condition2=0",
    "#class"   : tw6.Tw6SearchExtractor,
    "#pattern" : r"https://cdn\.tw6\.jp/i/tw6/(basic|thumb_grid)/\d+/\w+\.\w+",
    "#range"   : "1-100",
    "#count"   : 100,

    "search_tags": "かじゃねこ",
    "search"     : {
        "condition" : "0",
        "condition2": "0",
        "goods"     : "0",
        "main_job"  : "0",
        "max"       : "0",
        "min"       : "10",
        "race"      : "0",
        "sex"       : "0",
        "sort"      : "0",
        "sub_job"   : "0",
        "word"      : "かじゃねこ",
    },
},

)
