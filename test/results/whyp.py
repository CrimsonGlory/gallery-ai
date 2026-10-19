# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import whyp


__tests__ = (
{
    "#url"     : "https://whyp.it/tracks/13721/fallout-3-intro-remake",
    "#class"   : whyp.WhypAudioExtractor,
    "#pattern" : r"https://cdn.whyp.it/5e9de576-f33a-40ea-bd43-1693a568a6a0.mp3\?token=.+",

    "allow_downloads": False,
    "artwork_url"    : None,
    "artwork_url_fallback": "https://cdn.whyp.it/a46f3485-8d19-4753-98e0-76011c7e33b0.jpg",
    "comments_count" : int,
    "created_at"     : "2025-11-24T16:59:50+00:00",
    "date"           : "dt:2025-11-24 16:59:50",
    "description"    : "",
    "duration"       : 46.34,
    "extension"      : "mp3",
    "filename"       : "5e9de576-f33a-40ea-bd43-1693a568a6a0",
    "id"             : 13721,
    "lossless_size"  : None,
    "lossless_url"   : None,
    "lossy_size"     : 1853719,
    "lossy_url"      : r"re:https://cdn.whyp.it/5e9de576-f33a-40ea-bd43-1693a568a6a0.mp3",
    "original"       : False,
    "public"         : True,
    "settings_comments": "users",
    "slug"           : "fallout-3-intro-remake",
    "title"          : "Fallout 3 Intro Remake",
    "token"          : None,
    "user_id"        : 1,
    "waveform_url"   : r"re:https://cdn.whyp.it/5e9de576-f33a-40ea-bd43-1693a568a6a0.json",
    "user"           : {
        "avatar"          : "https://cdn.whyp.it/a46f3485-8d19-4753-98e0-76011c7e33b0.jpg",
        "?has_enterprise" : True,
        "has_pro"         : True,
        "?has_pro_lifetime": False,
        "id"              : 1,
        "slug"            : "brad",
        "status"          : "Coding 👨🏻‍💻",
        "username"        : "Brad",
    },
},

{
    "#url"     : "https://whyp.it/tracks/12345?token=tokenstring",
    "#comment" : "'token' paraneter (#9133)",
    "#class"   : whyp.WhypAudioExtractor,
},

{
    "#url"     : "https://whyp.it/tracks/12345/slug-of-track-title?token=tokenstring",
    "#comment" : "'token' paraneter (#9133)",
    "#class"   : whyp.WhypAudioExtractor,
},

{
    "#url"     : "https://whyp.it/tracks/example-track-HPuZgly3yViP",
    "#class"   : whyp.WhypAudioExtractor,
    "#pattern" : r"https://cdn\.whyp\.it/5670da67-2254-42f9-8bfc-3a512e0c18b8\.flac\?token=.+",

    "accent"          : None,
    "allow_downloads" : True,
    "artwork_url"     : str,
    "artwork_url_fallback": "https://cdn.whyp.it/a46f3485-8d19-4753-98e0-76011c7e33b0.jpg",
    "audio_changed_at": "2026-08-19T22:53:23+00:00",
    "comments_count"  : range(5, 50),
    "created_at"      : "2022-01-26T17:03:03+00:00",
    "date"            : "dt:2022-01-26 17:03:03",
    "duration"        : 135.629,
    "embed_signature" : "2d835866bff1207ff97c74420ce9adbd",
    "extension"       : "flac",
    "filename"        : "5670da67-2254-42f9-8bfc-3a512e0c18b8",
    "id"              : 18337,
    "lossless_size"   : 23236941,
    "lossless_url"    : r"re:https://cdn\.whyp\.it/5670da67-2254-42f9-8bfc-3a512e0c18b8\.flac\?token=.+",
    "lossy_size"      : 5428289,
    "lossy_url"       : r"re:https://cdn\.whyp\.it/5670da67-2254-42f9-8bfc-3a512e0c18b8\.mp3\?token=.+",
    "original"        : True,
    "public"          : True,
    "public_id"       : "HPuZgly3yViP",
    "public_versions_count": 1,
    "settings_comments": str,
    "slug"            : "example-track",
    "title"           : "Example Track",
    "token"           : None,
    "url"             : "/tracks/example-track-HPuZgly3yViP",
    "user_id"         : 1,
    "version_name"    : None,
    "waveform_url"    : r"re:https://cdn\.whyp\.it/5670da67-2254-42f9-8bfc-3a512e0c18b8\.json\?token=.+",
    "description"     : """\
An example track on Whyp.

00:15 awesome!

Credit: https://thetestdata.com/sample-flac-file-download.php\
""",
    "user"            : {
        "avatar"          : "https://cdn.whyp.it/a46f3485-8d19-4753-98e0-76011c7e33b0.jpg",
        "?has_enterprise" : True,
        "has_pro"         : True,
        "?has_pro_lifetime": False,
        "id"              : 1,
        "profile_accent"  : None,
        "public_id"       : "cGgThTrh8wcG",
        "slug"            : "brad",
        "status"          : "Coding 👨🏻‍💻",
        "url"             : "/users/brad-cGgThTrh8wcG",
        "username"        : "Brad",
    },
},

{
    "#url"     : "https://whyp.it/users/1/brad",
    "#class"   : whyp.WhypUserExtractor,
    "#pattern" : r"https://cdn\.whyp\.it/[0-9a-f-]+\.(mp3|flac)\?token=.+",
    "#count"   : range(1, 5),

    "allow_downloads": bool,
    "artwork_url"    : {str, None},
    "artwork_url_fallback": str,
    "comments_count" : int,
    "created_at"     : "iso:dt",
    "date"           : "type:datetime",
    "description"    : str,
    "duration"       : float,
    "extension"      : {"mp3", "flac"},
    "filename"       : "iso:uuid",
    "id"             : int,
    "lossless_size"  : {int, None},
    "lossless_url"   : {str, None},
    "lossy_size"     : int,
    "lossy_url"      : str,
    "original"       : bool,
    "public"         : True,
    "settings_comments": str,
    "slug"           : str,
    "title"          : str,
    "token"          : {str, None},
    "user_id"        : 1,
    "waveform_url"   : str,
    "user"           : {
        "avatar"          : "https://cdn.whyp.it/a46f3485-8d19-4753-98e0-76011c7e33b0.jpg",
        "?has_enterprise" : True,
        "has_pro"         : True,
        "?has_pro_lifetime": False,
        "id"              : 1,
        "slug"            : "brad",
        "status"          : "Coding 👨🏻‍💻",
        "username"        : "Brad",
    },
},

{
    "#url"     : "https://whyp.it/users/brad-cGgThTrh8wcG",
    "#class"   : whyp.WhypUserExtractor,
},

{
    "#url"     : "https://whyp.it/collections/1/example-collection",
    "#class"   : whyp.WhypCollectionExtractor,
    "#pattern" : (
        r"https://cdn.whyp.it/5670da67-2254-42f9-8bfc-3a512e0c18b8.flac\?token=.+",
        r"https://cdn.whyp.it/0d7a196b-3e1a-4510-a4a4-6189c56ecb27.flac\?token=.+",
        r"https://cdn.whyp.it/5e9de576-f33a-40ea-bd43-1693a568a6a0.mp3\?token=.+",
    ),

    "extension"       : {"flac", "mp3"},
    "id"              : {13721, 18337, 324260},
    "original"        : bool,
    "pivot_collection_id": 1,
    "pivot_created_at": "iso:dt",
    "pivot_order"     : int,
    "public"          : True,
    "collection"      : {
        "artwork_url" : None,
        "artwork_url_fallback": "https://cdn.whyp.it/b42b34d3-5839-4a26-9c32-41e917f31f6b.jpg",
        "created_at"  : "2023-07-20T16:14:33+00:00",
        "description" : "This is an example collection on Whyp!",
        "duration"    : 398.929,
        "hidden_tracks_count": 0,
        "id"          : 1,
        "order"       : {1, 3},
        "public"      : True,
        "slug"        : "example-collection",
        "title"       : "Example Collection",
        "token"       : None,
        "tracks_count": 3,
        "updated_at"  : "iso:8601",
        "user_id"     : 1,
        "user"        : dict,
    },
    "user"            : {
        "avatar"          : "https://cdn.whyp.it/a46f3485-8d19-4753-98e0-76011c7e33b0.jpg",
        "?has_enterprise" : True,
        "has_pro"         : True,
        "?has_pro_lifetime": False,
        "id"              : 1,
        "slug"            : "brad",
        "status"          : "Coding 👨🏻‍💻",
        "?tracks_count"   : int,
        "username"        : "Brad",
    },
},

{
    "#url"     : "https://whyp.it/collections/example-collection-hNdBmugKbF85",
    "#class"   : whyp.WhypCollectionExtractor,
},

)
