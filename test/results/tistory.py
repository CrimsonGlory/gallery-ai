# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import tistory


__tests__ = (
{
    "#url"     : "https://sakuga.tistory.com/42",
    "#class"   : tistory.TistoryArticleExtractor,
    "#pattern" : r"https://t1\.daumcdn\.net/cfile/tistory/\w+",
    "#count"   : 79,

    "author"     : "아주르",
    "blog"       : "sakuga",
    "blog_id"    : "1532159",
    "count"      : 79,
    "cover"      : r"re:https://img1.daumcdn.net/thumb/R800x0/.+",
    "date"       : "dt:2014-09-30 14:21:25",
    "description": "「철완버디 DECODE(鉄腕fバーディー DECODE)」는, 유우키 마사미(ゆうきまさみ)씨의 동명 만화 「철완버디」를 원작으로 한 애니메이션이며, A-1 Pictures에서 애니화했다. 감독은 「노에인 또 하나의 너에게(ノエイン もうひとりの君へ)」로 수많은 작화 오타쿠들을 열광시킨 아카네 카즈키(赤根和樹)씨로, 이번 작품으로 2년의 공백을 비웃기라도 하는 듯, 노에인에 이은 파격적인 작화 애니로 업계에 부활했다. 캐릭터 디자인은 플래시 작화로 유명한 료치모(りょーちも)씨. 시리즈 구성은 오오기노 히로시(大野木寛), 미나카미 세이시(水上清資)씨. 메카닉 디자인은 사야마 요시노리(佐山善則)씨와 테라오 히로유키(寺尾洋之)씨가 담당했다.▲방송직전 특별 방송. 아카네 감독의 인터뷰와 료치모씨의 작업환경을 짧게 비추..",
    "extension"  : "",
    "file_url"   : str,
    "filename"   : str,
    "height"     : int,
    "id"         : 42,
    "num"        : range(1, 79),
    "section"    : "'만화·애니'",
    "tags"       : [],
    "title"      : "철완버디 DECODE, 부활하라 작화 애니여!",
    "txid"       : "1532159_42",
    "url"        : "https://sakuga.tistory.com/42",
    "width"      : int,
},

{
    "#url"     : "https://breezehu.tistory.com/1436",
    "#class"   : tistory.TistoryArticleExtractor,
    "#pattern" : r"https://blog\.kakaocdn\.net/dna/.+",
    "#count"   : 15,

    "author"     : "난짬뽕",
    "blog"       : "breezehu",
    "blog_id"    : "4351705",
    "count"      : 15,
    "date"       : "dt:2026-11-06 00:00:26",
    "description": "은미정은 시래기 전문점으로 입소문이 난 곳입니다. 인덕원 서울구치소 입구 바로 옆에 자리해 있는데요. 본점은 수원 권선구에 있다고 합니다. 은미정메뉴: 한우우거지해장국, 시래기영양비빔밥, 한우육개장 등주소: 경기 의왕시 벌모루길 1 243-7영업시간: 06:00~21:30문의: 0507 1337 9964며칠 전 남편이 과천에 회의를 왔다가, 퇴근길에 저와 함께 집으로 가게 되었는데요. 차가 많이 밀릴 것 같아 이곳 은미정에서 저녁을 먹고 가기로 했습니다. 은미정 메뉴로는 한우 우거지해장국과 시래기 영양밥, 시래기 불고기, 시래기 두루치기, 시래기불고기뚝배기 등이 있고, 여름 특선 메뉴로는 소바다시막국수와 비빔막국수도 눈에 띄었어요. 그중에서 저희가 선택한 메뉴는 한우 우거지해장국과 한우 육개장입니다. ..",
    "id"         : 1436,
    "section"    : "'맛집'",
    "title"      : "진한 육수의 한우 우거지해장국이 맛있는 시래기 전문점 은미정",
    "txid"       : "4351705_1436",
    "url"        : "https://breezehu.tistory.com/1436",
    "tags"       : [
        "서울구치소맛집",
        "시래기전문점",
        "은미정",
        "의왕맛집",
        "인덕원해장국",
        "한우우거지해장국",
        "한우육개장",
    ],
},

{
    "#url"     : "https://cressu.tistory.com/entry/%EB%AF%B8%EB%8B%88%EB%A9%80%EB%9D%BC%EC%9D%B4%ED%94%84-%EC%88%98%EA%B1%B4-%EC%B9%A8%EA%B5%AC%EB%A5%98-%EA%B5%90%EC%B2%B4%EC%A3%BC%EA%B8%B0-%EB%8D%9C%EB%B9%A8%EC%95%84%EB%8F%84-%EB%90%98%EB%8A%94%EA%B2%83%EB%93%A4",
    "#class"   : tistory.TistoryArticleExtractor,
    "#pattern" : r"https://blog.kakaocdn.net/dna/.+",
    "#count"   : 4,

    "author"     : "크로수",
    "blog"       : "cressu",
    "blog_id"    : "3815566",
    "count"      : 4,
    "date"       : "dt:2026-11-04 07:46:56",
    "description": "빨래 바구니는 비우면 또 차 있고, 건조대는 늘 수건과 이불 커버가 차지하고 있죠. 그런데 가만히 생각해 보면 우리를 지치게 하는 건 '세탁 횟수'보다 '빨래가 되어 돌아오는 물건의 개수'인 경우가 많아요. 오늘은 수건과 침구를 얼마나 자주 빨아야 하는지부터, 물건을 줄여서 빨래 자체를 줄이는 미니멀 살림법까지 현실적으로 정리해 볼게요.목차1. 빨래가 많은 진짜 이유는 '개수'예요2. 수건: 몇 장이면 충분하고, 얼마나 자주 빨까?3. 침구류: 부위별 세탁 주기와 '2세트 로테이션'4. 행주·발매트·잠옷, 그리고 덜 빨아도 되는 것들5. 체력 0%에도 굴러가는 한 달 빨래 루틴6. 결론7. FAQ 1. 빨래가 많은 진짜 이유는 '개수'예요세탁 주기를 아무리 잘 지켜도, 수건이 서랍에 20장씩 있고 침구 ..",
    "filename"   : "img",
    "id"         : 0,
    "section"    : "'생활정보'",
    "title"      : "[미니멀라이프] 수건, 침구류 교체 주기 (알고 보면 덜 빨아도 되는 것들)",
    "txid"       : "3815566_345",
    "url"        : "https://cressu.tistory.com/entry/%EB%AF%B8%EB%8B%88%EB%A9%80%EB%9D%BC%EC%9D%B4%ED%94%84-%EC%88%98%EA%B1%B4-%EC%B9%A8%EA%B5%AC%EB%A5%98-%EA%B5%90%EC%B2%B4%EC%A3%BC%EA%B8%B0-%EB%8D%9C%EB%B9%A8%EC%95%84%EB%8F%84-%EB%90%98%EB%8A%94%EA%B2%83%EB%93%A4",
    "tags"       : [
        "미니멀 라이프",
        "빨래 줄이기",
        "수건 세탁주기",
        "이불 세탁주기",
        "침대 세탁주기",
    ],
},

{
    "#url"     : "https://sakuga.tistory.com/",
    "#class"   : tistory.TistoryBlogExtractor,
    "#pattern" : tistory.TistoryArticleExtractor.pattern,
    "#count"   : 54,
},

{
    "#url"     : "https://cressu.tistory.com/",
    "#class"   : tistory.TistoryBlogExtractor,
    "#pattern" : tistory.TistoryArticleExtractor.pattern,
    "#range"   : "1-50",
    "#count"   : 50,
},

{
    "#url"     : "http://cfile7.uf.tistory.com/original/02422B4E51876F2C200ABC",
    "#class"   : tistory.TistoryDirectLinkExtractor,
    "#results" : "http://cfile7.uf.tistory.com/original/02422B4E51876F2C200ABC",
},

{
    "#url"     : "http://cfile7.uf.tistory.com/image/02422B4E51876F2C200ABC",
    "#class"   : tistory.TistoryDirectLinkExtractor,
    "#results" : "http://cfile7.uf.tistory.com/image/02422B4E51876F2C200ABC",
},

{
    "#url"     : "http://cfile7.uf.tistory.com/attach/02422B4E51876F2C200ABC",
    "#class"   : tistory.TistoryDirectLinkExtractor,
    "#results" : "http://cfile7.uf.tistory.com/attach/02422B4E51876F2C200ABC",
},

{
    "#url"     : "http://cfile7.uf.tistory.com/media/02422B4E51876F2C200ABC",
    "#class"   : tistory.TistoryDirectLinkExtractor,
    "#results" : "http://cfile7.uf.tistory.com/media/02422B4E51876F2C200ABC",
},

{
    "#url"     : "https://t1.daumcdn.net/cfile/tistory/21747B4B574C16920A?original",
    "#class"   : tistory.TistoryDirectLinkExtractor,
    "#results" : "https://t1.daumcdn.net/cfile/tistory/21747B4B574C16920A?original",
},

{
    "#url"     : "http://cfile208.uf.daum.net/original/233F654453F6F5220CD5AE",
    "#class"   : tistory.TistoryDirectLinkExtractor,
    "#results" : "http://cfile208.uf.daum.net/original/233F654453F6F5220CD5AE",
},

)
