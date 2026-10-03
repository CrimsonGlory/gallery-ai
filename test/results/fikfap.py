# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import fikfap


__tests__ = (
{
    "#url"     : "https://fikfap.com/user/alinevs/post/1429486",
    "#class"   : fikfap.FikfapPostExtractor,
    "#pattern" : r"ytdl:https://vz-\w+-178\.b-cdn\.net/bcdn_token=.+/playlist\.m3u8",

    "algorithm"      : "single-post",
    "bunnyVideoId"   : "89218ae2-d79a-49a0-abcd-590fd70c9800",
    "commentsCount"  : int,
    "createdAt"      : "2025-10-21T00:49:00.306Z",
    "date"           : "dt:2025-10-21 00:49:00",
    "date_updated"   : "type:datetime",
    "deletedAt"      : None,
    "duration"       : None,
    "explicitnessRating": {None, "FULLY_EXPLICIT", "PARTIALLY_EXPLICIT"},
    "extension"      : "mp4",
    "filename"       : "⬇️check my FREE VIP OF ⬇️",
    "inCollectionsCount": range(20, 50),
    "isBunnyVideoReady": True,
    "label"          : "⬇️check my FREE VIP OF ⬇️",
    "likesCount"     : range(100, 2000),
    "mediaId"        : "b821619e-96a1-49a3-a3f8-a8a3e8432a51",
    "postId"         : 1429486,
    "publishedAt"    : "2025-10-21T00:50:37.143Z",
    "score"          : range(100, 2000),
    "sexualOrientation": "STRAIGHT",
    "tags"           : ["lesbian"],
    "thumbnailStreamUrl": str,
    "updatedAt"      : "iso:dt",
    "uploadMethod"   : "USER_FILE",
    "userId"         : "32f4c8d6-2409-4db8-9e66-d3b5ff0c1a98",
    "videoStreamUrl" : str,
    "viewsCount"     : range(40_000, 200_000),
    "hashtags"       : [{
        "createdAt"      : "2023-09-05T11:03:49.522Z",
        "description"    : "Lesbian content only.",
        "hashtagId"      : "287439f9-3210-42e2-98ea-2c7a86628845",
        "isModerated"    : True,
        "label"          : "lesbian",
        "labelLower"     : "lesbian",
        "lastCountUpdatedAt": "iso:dt",
        "searchTags"     : [],
        "thumbnailPostId": 311180,
        "updatedAt"      : "iso:dt",
        "sexualOrientations": [
            "STRAIGHT",
            "LESBIAN",
            "TRANS",
            "OTHER",
        ],
    }],
    "author"         : {
        "countCollections": 1,
        "countIncomingFollows": int,
        "countIncomingLikes"  : int,
        "countOutgoingFollows": int,
        "countOutgoingLikes"  : int,
        "countPosts"      : int,
        "countTotalViews" : int,
        "createdAt"       : "2023-05-20T15:45:08.702Z",
        "deletedAt"       : None,
        "description"     : str,
        "isAmbassador"    : False,
        "isPartner"       : True,
        "isSignedUp"      : True,
        "isStaff"         : False,
        "isVerified"      : True,
        "lastSeenAt"      : "iso:dt",
        "roles"           : [],
        "thumbnailId"     : "b4b4f444-71d9-4dcd-91e4-0466ff5b9cdd",
        "thumbnailUrl"    : str,
        "updatedAt"       : "iso:dt",
        "userId"          : "32f4c8d6-2409-4db8-9e66-d3b5ff0c1a98",
        "username"        : "alinevs",
        "profileLinks"    : list,
    },
    "linkDescription": {
        "location"     : "POST_DESCRIPTION",
        "profileLinkId": str,
        "type"         : "ONLYFANS",
        "url"          : str,
        "userId"       : "32f4c8d6-2409-4db8-9e66-d3b5ff0c1a98",
    },
    "linkSidebar"    : {
        "location"     : "POST_SIDEBAR",
        "profileLinkId": str,
        "type"         : "OTHER",
        "url"          : str,
        "userId"       : "32f4c8d6-2409-4db8-9e66-d3b5ff0c1a98",
    },
},

{
    "#url"     : "https://fikfap.com/post/1429486",
    "#class"   : fikfap.FikfapPostExtractor,
    "#pattern" : r"ytdl:https://vz-\w+-178\.b-cdn\.net/bcdn_token=.+/playlist\.m3u8",

    "bunnyVideoId": "89218ae2-d79a-49a0-abcd-590fd70c9800",
    "date"        : "dt:2025-10-21 00:49:00",
    "extension"   : "mp4",
    "filename"    : "⬇️check my FREE VIP OF ⬇️",
    "mediaId"     : "b821619e-96a1-49a3-a3f8-a8a3e8432a51",
    "postId"      : 1429486,
    "userId"      : "32f4c8d6-2409-4db8-9e66-d3b5ff0c1a98",
},

{
    "#url"     : "https://fikfap.com/user/Hot-sauce-34/post/1026309",
    "#class"   : fikfap.FikfapPostExtractor,
},

{
    "#url"     : "https://fikfap.com/user/alinevs",
    "#class"   : fikfap.FikfapUserExtractor,
    "#range"   : "1-50",
    "#pattern" : r"ytdl:https://vz-\w+-\w+\.b\-cdn\.net/bcdn_token=.+/playlist\.m3u8",
    "#count"   : 50,

    "algorithm"      : "user-posts",
    "date"           : "type:datetime",
    "date_updated"   : "type:datetime",
    "extension"      : "mp4",
    "filename"       : str,
    "postId"         : int,
    "tags"           : list,
    "hashtags"       : list,
    "author"         : dict,
    "linkDescription": dict,
    "linkSidebar"    : dict,
},

{
    "#url"     : "https://fikfap.com/user/Hot-sauce-34",
    "#comment" : "'-' in username",
    "#class"   : fikfap.FikfapUserExtractor,
},

{
    "#url"     : "https://fikfap.com/hash/outercourse",
    "#class"   : fikfap.FikfapHashtagExtractor,
    "#pattern" : r"ytdl:https://[^/]+\.b\-cdn\.net/bcdn_token=.+/playlist\.m3u8$",
    "#count"   : range(50, 100),

    "algorithm": "hashtag-posts",
    "hashtag"  : "outercourse",
},

{
    "#url"     : "https://fikfap.com/hash/foo-bar",
    "#class"   : fikfap.FikfapHashtagExtractor,
},

)
