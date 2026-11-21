# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://www.share-image.com/"""

from .common import GalleryExtractor
from .. import text


class ShareimageGalleryExtractor(GalleryExtractor):
    """Extractor for image galleries from share-image.com"""
    category = "shareimage"
    root = "https://www.share-image.com"
    pattern = (r"(?:https?://)?(?:www\.)?share-image\.com"
               r"(/(?:galleries/|image/)?(\d+)[^/?#]*)")
    example = "https://www.share-image.com/galleries/12345-TITLE"

    def items(self):
        try:
            yield from GalleryExtractor.items(self)
        except self.exc.HttpError as exc:
            if exc.status == 410:
                raise self.exc.NotFoundError(self.subcategory)
            raise

    def metadata(self, page):
        self.schema = schema = self._extract_jsonld(page)
        return {
            "gallery_id" : text.parse_int(self.groups[1]),
            "gallery_url": schema.get("url"),
            "title"      : schema.get("name"),
        }

    def images(self, page):
        schema = self.schema
        media = schema.get("associatedMedia")
        if media.__class__ is list:
            images = []
            for item in media:
                if item.__class__ is dict:
                    url = item.get("contentUrl")
                    if url:
                        images.append((url, None))
            if images:
                return images
        images = schema.get("image")
        if images.__class__ is str:
            images = (images,)
        if images:
            return [(url, None) for url in images]
        url = schema.get("contentUrl")
        if url:
            return [(url, None)]
        raise self.exc.NotFoundError(self.subcategory)
