# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://thefap.net/"""

from .common import Extractor, Message
from .. import text

BASE_PATTERN = r"(?:https?://)?(?:www\.)?thefap\.net"


class ThefapExtractor(Extractor):
    """Base class for thefap extractors"""
    category = "thefap"
    root = "https://thefap.net"
    directory_fmt = ("{category}", "{model_name} ({model_id})")
    filename_fmt = "{model}_{num:>03}.{extension}"
    archive_fmt = "{model_id}_{filename}"

    def _normalize_url(self, url):
        if not url:
            return ""
        url = url.strip()
        if "?w=" in url:
            url = url[:url.rfind("?")]
        elif url.endswith(":small"):
            url = url[:-6] + ":orig"
        if url.startswith("//"):
            url = "https:" + url
        elif url.startswith("/"):
            url = self.root + url
        return url

    def _is_media(self, url):
        if any(s in url for s in (
                "/assets/", "whos.amung.us", "earringsatisfiedsplice",
                "googleads", "doubleclick", "gravatar.com")):
            return False
        path = url.split("?", 1)[0].lower()
        return path.endswith((
            ".jpg", ".jpeg", ".png", ".gif", ".webp", ".mp4", ".webm",
            ":orig")) or "twimg.com" in url or "i.redd.it" in url or \
            "pixhost" in url


class ThefapPostExtractor(ThefapExtractor):
    """Extractor for individual thefap.net posts"""
    subcategory = "post"
    pattern = (BASE_PATTERN +
               r"(/([^/?#]+)-(\d+)/([^/?#]+)/i(\d+))")
    example = "https://thefap.net/MODEL-12345/KIND/i12345"

    def items(self):
        path, model, model_id, kind, post_id = self.groups

        page = self.request(self.root + path).text
        if "Not Found" in page or "Content removed" in page or \
                "/assets/images/removed.png" in page:
            raise self.exc.NotFoundError("post")

        if model_name := text.extr(page, "<title>", " / "):
            model_name = text.unescape(model_name)
        else:
            model_name = text.unquote(model).replace(".", " ")

        data = {
            "model"     : model,
            "model_id"  : text.parse_int(model_id),
            "model_name": model_name,
            "kind"      : kind,
            "post_id"   : text.parse_int(post_id),
            "_http_headers": {"Referer": None},
        }
        yield Message.Directory, "", data

        data["num"] = 0
        start = page.find("</header>")
        chunk = page[start:] if start >= 0 else page
        for marker in ('id="content"', "uk-divider-icon", "<footer"):
            pos = chunk.find(marker, 200)
            if pos > 0:
                chunk = chunk[:pos]
                break
        seen = set()
        for attr in ('src="', 'data-src="'):
            for url in text.extract_iter(chunk, attr, '"'):
                if url := self._normalize_url(url):
                    if url in seen or not self._is_media(url):
                        continue
                    seen.add(url)
                    data["num"] += 1
                    yield Message.Url, url, text.nameext_from_url(url, data)


class ThefapModelExtractor(ThefapExtractor):
    """Extractor for thefap.net model pages"""
    subcategory = "model"
    pattern = BASE_PATTERN + r"/([^/?#]+)-(\d+)"
    example = "https://thefap.net/MODEL-12345/"

    def items(self):
        model, model_id = self.groups

        url = f"{self.root}/{model}-{model_id}/"
        page = self.request(url).text

        if 'id="content"' not in page:
            raise self.exc.NotFoundError("model")

        if model_name := text.extr(page, "<h2", "</h2>"):
            model_name = text.unescape(model_name[model_name.find(">")+1:])
        else:
            model_name = text.unquote(model).replace(".", " ")

        data = {
            "model"     : model,
            "model_id"  : text.parse_int(model_id),
            "model_name": model_name,
            "_http_headers": {"Referer": None},
        }
        yield Message.Directory, "", data

        base = f"{self.root}/ajax/model/{model_id}/page-"
        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Sec-Fetch-Dest"  : "empty",
            "Sec-Fetch-Mode"  : "cors",
            "Sec-Fetch-Site"  : "same-origin",
        }

        start = page.find('id="content"')
        chunk = page[start:] if start >= 0 else ""
        for marker in ('id="showmore"', "<footer", "</main>"):
            pos = chunk.find(marker, 100)
            if pos > 0:
                chunk = chunk[:pos]
                break
        imgs = list(text.extract_iter(chunk, 'data-src="', '"'))
        if not imgs:
            imgs = [u for u in text.extract_iter(chunk, '<img src="', '"')
                    if "/assets/" not in u]
        pnum = 1
        data["num"] = 0

        while True:
            for url in imgs:
                if url := self._normalize_url(url):
                    data["num"] += 1
                    yield Message.Url, url, text.nameext_from_url(url, data)

            pnum += 1
            page = self.request(base + str(pnum), headers=headers).text
            if not page:
                break
            imgs = list(text.extract_iter(page, 'data-src="', '"'))
            if not imgs:
                imgs = [u for u in text.extract_iter(page, '<img src="', '"')
                        if "/assets/" not in u]
            if not imgs:
                break
