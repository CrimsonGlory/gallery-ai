# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for general-purpose URL shorteners"""

from .common import BaseExtractor, Message
from .. import text


class UrlshortenerExtractor(BaseExtractor):
    """Base class for URL shortener extractors"""
    basecategory = "urlshortener"


BASE_PATTERN = UrlshortenerExtractor.update({
    "bitly": {
        "root": "https://bit.ly",
        "pattern": r"bit\.ly",
    },
    "tco": {
        # t.co sends 'http-equiv="refresh"' (200) when using browser UA
        # Empty UA (not None: curl_cffi drops None) gets a 301 Location.
        "headers": {"User-Agent": ""},
        "root": "https://t.co",
        "pattern": r"t\.co",
    },
})


class UrlshortenerLinkExtractor(UrlshortenerExtractor):
    """Extractor for general-purpose URL shorteners"""
    subcategory = "link"
    pattern = BASE_PATTERN + r"(/[^/?#]+)"
    example = "https://bit.ly/abcde"

    def items(self):
        url = self.root + self.groups[-1]
        headers = self.config_instance("headers")
        location = self.request_location(
            url, headers=headers, notfound="URL")
        if not location:
            # t.co returns 200 + meta refresh for browser-like User-Agents
            location = text.extr(
                self.request(url, headers=headers).text, "URL=", '"')
        if not location:
            raise self.exc.AbortExtraction("Unable to resolve short URL")
        yield Message.Queue, location, {}
