# -*- coding: utf-8 -*-

# Copyright 2014-2026 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://www.imagebam.com/"""

from .common import Extractor, Message
from .. import text


class ImagebamExtractor(Extractor):
    """Base class for imagebam extractors"""
    category = "imagebam"
    root = "https://www.imagebam.com"

    def __init__(self, match):
        Extractor.__init__(self, match)
        self.path = match[1]

    def _init(self):
        for domain in (".imagebam.com", "www.imagebam.com", "imagebam.com"):
            self.cookies.set("nsfw_inter", "1", domain=domain)
            self.cookies.set("sfw_inter", "1", domain=domain)

    def _parse_image_page(self, path):
        page = self.request(self.root + path, notfound="image").text
        url, pos = text.extract(page, '<img src="https://images', '"')
        if not url:
            url, pos = text.extract(
                page, 'og:image" content="https://images', '"')
        if not url:
            url, pos = text.extract(page, '<img src="https://thumbs', '"')
            if url:
                url = url.replace("://thumbs", "://images", 1)
        if not url:
            raise self.exc.NotFoundError("image")
        filename = text.unescape(text.extract(page, 'alt="', '"', pos)[0])

        return text.nameext_from_name(filename, {
            "url"      : "https://images" + url,
            "image_key": path.rpartition("/")[2],
        })


class ImagebamGalleryExtractor(ImagebamExtractor):
    """Extractor for imagebam galleries"""
    subcategory = "gallery"
    directory_fmt = ("{category}", "{title} {gallery_key}")
    filename_fmt = "{num:>03} {filename}.{extension}"
    archive_fmt = "{gallery_key}_{image_key}"
    pattern = (r"(?:https?://)?(?:www\.)?imagebam\.com"
               r"(/(?:gallery/|view/G)[a-zA-Z0-9]+)")
    example = "https://www.imagebam.com/view/GID"

    def items(self):
        page = self.request(self.root + self.path, notfound=True).text

        images = self.images(page)
        images.reverse()

        data = self.metadata(page)
        data["count"] = len(images)
        data["gallery_key"] = self.path.rpartition("/")[2]

        yield Message.Directory, "", data
        num = 0
        for path in images:
            if path.startswith("http"):
                image = text.nameext_from_url(path, {
                    "url"      : path,
                    "image_key": path.rsplit("/", 1)[-1].split(".", 1)[0],
                })
            else:
                try:
                    image = self._parse_image_page(path)
                except self.exc.NotFoundError as exc:
                    self.log.warning("%s: %s", path, exc)
                    continue
            num += 1
            data["num"] = num
            image.update(data)
            yield Message.Url, image["url"], image
        data["count"] = num

    def metadata(self, page):
        return {"title": text.unescape(text.extr(
            page, 'id="gallery-name">', '<').strip())}

    def images(self, page):
        paths = []
        while True:
            thumbs = text.re(
                r'https://thumbs\d+\.imagebam\.com/'
                r'[A-Za-z0-9_./-]+\.(?:jpe?g|png|gif|webp)'
                ).findall(page)
            if thumbs:
                found = [url.replace("://thumbs", "://images", 1)
                         for url in thumbs]
            else:
                found = text.re(
                    r'<a href="https://(?:www\.)?imagebam\.com'
                    r'(/(?:image/|view/M)[a-zA-Z0-9]+)').findall(page)
            for path in found:
                if path not in paths:
                    paths.append(path)
            pos = page.find('rel="next" aria-label="Next')
            if pos > 0:
                if url := text.rextr(page, 'href="', '"', pos):
                    page = self.request(url).text
                    continue
            return paths


class ImagebamImageExtractor(ImagebamExtractor):
    """Extractor for single imagebam images"""
    subcategory = "image"
    archive_fmt = "{image_key}"
    pattern = (r"(?:https?://)?(?:\w+\.)?imagebam\.com"
               r"(/(?:image/|view/M|(?:[0-9a-f]{2}/){3})[a-zA-Z0-9]+)")
    example = "https://www.imagebam.com/view/MID"

    def items(self):
        path = self.path
        if path[3] == "/":
            path = ("/view/" if path[10] == "M" else "/image/") + path[10:]

        image = self._parse_image_page(path)
        yield Message.Directory, "", image
        yield Message.Url, image["url"], image
