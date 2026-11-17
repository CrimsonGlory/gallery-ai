# -*- coding: utf-8 -*-

# Copyright 2016-2026 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://www.pixnet.net/"""

from .common import Extractor, Message
from .. import text

BASE_PATTERN = r"(?:https?://)?(?!www\.)([\w-]+)\.pixnet.net"
GALLERY_ITEM_RE = text.re(
    r'<a href="([^"]+)" data-photo-id="(\d+)" data-title="([^"]*)"'
    r'[^>]*class="gallery-item"')
NEXT_LIST_RE = text.re(r'<a href="([^"]+)" class="next">»</a>')
NEXT_SET_RE = text.re(
    r'<a href="([^"]+)" data-slot="pagination-link"')


class PixnetExtractor(Extractor):
    """Base class for pixnet extractors"""
    category = "pixnet"
    filename_fmt = "{num:>03}_{id}.{extension}"
    archive_fmt = "{id}"

    def __init__(self, match):
        Extractor.__init__(self, match)
        self.blog = self.groups[0]
        self.item_id = next((g for g in self.groups[1:] if g), "")
        self.root = f"https://{self.blog}.pixnet.net"

    def items(self):
        url = self._page_url()
        page = self._request_page(url)[1]
        data = self._user_data(page)

        folders = self._folders(page)
        if folders:
            for fid, title in folders:
                item = {
                    "id"        : text.parse_int(fid),
                    "title"     : title,
                    "_extractor": PixnetFolderExtractor,
                }
                item.update(data)
                yield Message.Queue, (
                    f"{self.root}/albums?folderId={fid}"), item
            return

        for set_url, title, set_id in self._iter_sets(url, page):
            item = {
                "id"        : set_id,
                "title"     : title,
                "_extractor": PixnetSetExtractor,
            }
            item.update(data)
            yield Message.Queue, set_url, item

    def _page_url(self):
        return self.url_fmt.format(self.root, self.item_id)

    def _request_page(self, url, notfound=True):
        response = self.request(url, encoding="utf-8", notfound=notfound)
        page = response.text
        if "這是一個私密的部落格" in page:
            raise self.exc.AuthorizationError("Private blog")
        if 'name="albumpass">' in page:
            raise self.exc.AbortExtraction(
                f"Album {self.item_id} is password-protected.")
        return response, page

    def _user_data(self, page):
        user = (text.extr(page, '<meta name="author" content="', '"') or
                text.extr(page, '<meta name="article:author" content="', '"'))
        return {
            "blog": self.blog,
            "user": user,
        }

    def _folders(self, page):
        select = text.extr(page, 'name="folderId"', "</select>")
        if not select:
            return ()
        folders = []
        for opt in text.extract_iter(select, '<option value="', "</option>"):
            fid, _, title = opt.partition('"')
            if fid.isdigit():
                folders.append((fid, text.unescape(title).strip()))
        return folders

    def _iter_sets(self, url, page):
        needle = f'<a href="{self.root}/albums/'
        while True:
            for info in text.extract_iter(page, needle, "</a>"):
                album_id, _, rest = info.partition('"')
                if not album_id.isdigit():
                    continue
                title = text.extr(rest, 'data-slot="card-title"', "</div>")
                title = text.unescape(text.extr(title, ">", "")).strip()
                yield (f"{self.root}/albums/{album_id}",
                       title, text.parse_int(album_id))

            url = self._next_url(page, url)
            if not url:
                return
            page = self._request_page(url)[1]

    def _iter_photos(self, url, page):
        while True:
            for photo_url, photo_id, title in GALLERY_ITEM_RE.findall(page):
                yield photo_url, photo_id, text.unescape(title)

            url = self._next_url(page, url)
            if not url:
                return
            page = self._request_page(url)[1]

    def _next_url(self, page, url):
        nxt = NEXT_LIST_RE.search(page)
        if nxt:
            return text.unescape(nxt[1])

        current = text.parse_int(text.extr(
            url.replace("?", "&") + "&", "page=", "&"), 1)
        for href in NEXT_SET_RE.findall(page):
            href = text.unescape(href)
            page_n = text.parse_int(text.extr(
                href.replace("?", "&") + "&", "page=", "&"), 0)
            if page_n == current + 1:
                return href
        return None


class PixnetImageExtractor(PixnetExtractor):
    """Extractor for a single photo from pixnet.net"""
    subcategory = "image"
    filename_fmt = "{id}.{extension}"
    directory_fmt = ("{category}", "{blog}")
    pattern = BASE_PATTERN + r"/(?:album/photo/|albums/\d+/photos/)(\d+)"
    example = "https://USER.pixnet.net/album/photo/12345"

    def items(self):
        response, page = self._request_page(self.url, notfound="image")
        photo_id = self.item_id
        needle = f'data-photo-id="{photo_id}"'
        album_url = response.url
        if "/photos/" in album_url:
            album_url = album_url.split("/photos/")[0]

        while needle not in page:
            nxt = self._next_url(page, album_url)
            if not nxt:
                raise self.exc.NotFoundError("image")
            album_url = nxt
            page = self._request_page(nxt, notfound="image")[1]

        pos = page.find(needle)
        photo_url = text.extr(page[max(0, pos-400):pos], 'href="', '"')
        if not photo_url:
            raise self.exc.NotFoundError("image")
        title = text.unescape(text.extr(
            page, needle + ' data-title="', '"'))
        data = text.nameext_from_name(title, self._user_data(page))
        data["id"] = text.parse_int(photo_id)
        data["url"] = photo_url

        yield Message.Directory, "", data
        yield Message.Url, photo_url, data


class PixnetSetExtractor(PixnetExtractor):
    """Extractor for images from a pixnet set"""
    subcategory = "set"
    directory_fmt = ("{category}", "{blog}",
                     "{folder_id} {folder_title}", "{set_id} {set_title}")
    pattern = BASE_PATTERN + r"/(?:album/set/|albums/)(\d+)/?(?:$|[?#])"
    example = "https://USER.pixnet.net/album/set/12345"

    def items(self):
        url = f"{self.root}/albums/{self.item_id}"
        response, page = self._request_page(url)
        if f'"album_id":"{self.item_id}"' not in page:
            raise self.exc.NotFoundError("set")
        data = self.metadata(page)

        yield Message.Directory, "", data
        num = 0
        for photo_url, photo_id, title in self._iter_photos(response.url, page):
            num += 1
            photo = text.nameext_from_name(title, {
                "id" : text.parse_int(photo_id),
                "url": photo_url,
                "num": num,
            })
            photo.update(data)
            yield Message.Url, photo_url, photo

    def metadata(self, page):
        data = self._user_data(page)
        title = text.unescape(text.extr(
            text.extr(page, "<h2", "</h2>"), ">", "")).strip()
        if title.endswith(" 的相簿照片"):
            title = title[:-6]
        if not title:
            title = text.unescape(text.extr(
                page, '<meta property="og:title" content="', '"'))
            title = title.split(" | ", 1)[0]
        data["folder_id"] = ""
        data["folder_title"] = ""
        data["set_id"] = text.parse_int(self.item_id)
        data["set_title"] = title.strip()
        return data


class PixnetFolderExtractor(PixnetExtractor):
    """Extractor for all sets in a pixnet folder"""
    subcategory = "folder"
    url_fmt = "{}/albums?folderId={}"
    pattern = (BASE_PATTERN +
               r"/(?:album/folder/(\d+)|albums/?\?(?:[^#]*&)?folderId=(\d+))")
    example = "https://USER.pixnet.net/album/folder/12345"

    def items(self):
        url = self._page_url()
        page = self._request_page(url)[1]
        data = self._user_data(page)
        for set_url, title, set_id in self._iter_sets(url, page):
            item = {
                "id"        : set_id,
                "title"     : title,
                "folder_id" : text.parse_int(self.item_id),
                "_extractor": PixnetSetExtractor,
            }
            item.update(data)
            yield Message.Queue, set_url, item


class PixnetUserExtractor(PixnetExtractor):
    """Extractor for all sets and folders of a pixnet user"""
    subcategory = "user"
    url_fmt = "{}/albums"
    pattern = BASE_PATTERN + r"()(?:/blog|/albums?|/album/list)?/?(?:$|[?#])"
    example = "https://USER.pixnet.net/"
