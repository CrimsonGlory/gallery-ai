#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018-2026 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import os
import sys
import unittest
from unittest.mock import patch

import time
import string

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gallery_dl import extractor, util, dt, config, cache  # noqa E402
from gallery_dl.extractor import mastodon  # noqa E402
from gallery_dl.extractor.common import Extractor, Message  # noqa E402
from gallery_dl.extractor.directlink import DirectlinkExtractor  # noqa E402

_list_classes = extractor._list_classes

try:
    RESULTS = os.environ.get("GDL_TEST_RESULTS")
    if RESULTS:
        results = util.import_file(RESULTS)
    else:
        from test import results
except ImportError:
    results = None


def setUpModule():
    if cache.DATABASE is None:
        import atexit
        import tempfile
        dbpath = tempfile.mkstemp()[1]
        config.set(("cache",), "file", dbpath)
        atexit.register(util.remove_file, dbpath)


class FakeExtractor(Extractor):
    category = "fake"
    subcategory = "test"
    pattern = "fake:"

    def items(self):
        yield Message.Noop
        yield Message.Url, "text:foobar", {}


class TestExtractorModule(unittest.TestCase):
    VALID_URIS = (
        "https://example.org/file.jpg",
        "tumblr:foobar",
        "oauth:flickr",
        "generic:https://example.org/",
        "recursive:https://example.org/document.html",
    )

    def setUp(self):
        extractor._cache.clear()
        extractor._module_iter = extractor._modules_internal()
        extractor._list_classes = _list_classes

    def test_find(self):
        for uri in self.VALID_URIS:
            result = extractor.find(uri)
            self.assertIsInstance(result, Extractor, uri)

        for not_found in ("", "/tmp/file.ext"):
            self.assertIsNone(extractor.find(not_found))

        for invalid in (None, [], {}, 123, b"test:"):
            with self.assertRaises(TypeError):
                extractor.find(invalid)

    def test_add(self):
        uri = "fake:foobar"
        self.assertIsNone(extractor.find(uri))

        extractor.add(FakeExtractor)
        self.assertIsInstance(extractor.find(uri), FakeExtractor)

    def test_add_module(self):
        uri = "fake:foobar"
        self.assertIsNone(extractor.find(uri))

        classes = extractor.add_module(sys.modules[__name__])
        self.assertEqual(len(classes), 1)
        self.assertEqual(classes[0].pattern, FakeExtractor.pattern)
        self.assertEqual(classes[0], FakeExtractor)
        self.assertIsInstance(extractor.find(uri), FakeExtractor)

    def test_from_url(self):
        for uri in self.VALID_URIS:
            cls = extractor.find(uri).__class__
            extr = cls.from_url(uri)
            self.assertIs(type(extr), cls)
            self.assertIsInstance(extr, Extractor)

        for not_found in ("", "/tmp/file.ext"):
            self.assertIsNone(FakeExtractor.from_url(not_found))

        for invalid in (None, [], {}, 123, b"test:"):
            with self.assertRaises(TypeError):
                FakeExtractor.from_url(invalid)

    @unittest.skipIf(not results, "no test data")
    def test_categories(self):
        for result in results.all():
            if result.get("#fail"):
                try:
                    self.assertCategories(result)
                except AssertionError:
                    pass
                else:
                    self.fail(f"{result['#url']}: Test did not fail")
            else:
                self.assertCategories(result)

    def assertCategories(self, result):
        url = result["#url"]
        cls = result["#class"]

        try:
            extr = cls.from_url(url)
            find = extractor.find(url)
        except ImportError as exc:
            if exc.name in ("youtube_dl", "yt_dlp", "yt_ai"):
                return sys.stdout.write(
                    f"Skipping '{cls.category}' category checks\n")
            raise
        self.assertTrue(extr, url)
        if find is None:
            self.assertFalse(cls.__module__.startswith(
                "gallery_dl.extractor."), "external extractor")
        else:
            self.assertIs(extr.__class__, find.__class__, url)

        categories = result.get("#category")
        if categories:
            base, cat, sub = categories
        else:
            cat = cls.category
            sub = cls.subcategory
            base = cls.basecategory
        self.assertEqual(extr.category, cat, url)
        self.assertEqual(extr.subcategory, sub, url)
        self.assertEqual(extr.basecategory, base, url)

        if base not in ("reactor", "wikimedia"):
            self.assertEqual(extr._cfgpath, ("extractor", cat, sub), url)

    def test_init(self):
        """Test for exceptions in Extractor.initialize() and .finalize()"""
        def fail_request(*args, **kwargs):
            self.fail("called 'request() during initialization")

        for cls in extractor.extractors():
            if cls.category == "ytdl":
                continue
            extr = cls.from_url(cls.example)
            if not extr:
                if cls.basecategory and not cls.instances:
                    continue
                self.fail(f"{cls.__name__} pattern does not match "
                          f"example URL '{cls.example}'")

            self.assertEqual(cls, extr.__class__)
            self.assertEqual(cls, extractor.find(cls.example).__class__)

            extr.request = fail_request
            extr.initialize()
            if extr.finalize is not None:
                extr.finalize(0)

    def test_init_ytdl(self):
        try:
            extr = extractor.find("ytdl:")
            extr.initialize()
            if extr.finalize is not None:
                extr.finalize(0)
        except ImportError as exc:
            if exc.name in ("youtube_dl", "yt_dlp", "yt_ai"):
                raise unittest.SkipTest(f"cannot import module '{exc.name}'")
            raise

    def test_docstrings(self):
        """Ensure docstring uniqueness"""
        for extr1 in extractor.extractors():
            for extr2 in extractor.extractors():
                if extr1 != extr2 and extr1.__doc__ and extr2.__doc__:
                    self.assertNotEqual(
                        extr1.__doc__,
                        extr2.__doc__,
                        f"{extr1} <-> {extr2}",
                    )

    def test_names(self):
        """Ensure extractor classes are named CategorySubcategoryExtractor"""
        def capitalize(c):
            if "-" in c:
                return string.capwords(c.replace("-", " ")).replace(" ", "")
            return c.capitalize()

        for extr in extractor.extractors():
            if extr.category not in ("", "oauth", "ytdl"):
                expected = (f"{capitalize(extr.category)}"
                            f"{capitalize(extr.subcategory)}Extractor")
                if expected[0].isdigit():
                    expected = f"_{expected}"
                self.assertEqual(expected, extr.__name__)


class TestExtractorWait(unittest.TestCase):

    def test_wait_seconds(self):
        extr = extractor.find("generic:https://example.org/")
        seconds = 5
        until = time.time() + seconds

        with patch("time.sleep") as sleep, patch.object(extr, "log") as log:
            extr.wait(seconds=seconds)

            sleep.assert_called_once_with(6.0)

            calls = log.info.mock_calls
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0][1][1], "6 seconds")
            self._assert_isotime(calls[0][1][2], until)

    def test_wait_seconds_long(self):
        extr = extractor.find("generic:https://example.org/")
        seconds = 5000
        until = time.time() + seconds

        with patch("time.sleep") as sleep, patch.object(extr, "log") as log:
            extr.wait(seconds=seconds)

            sleep.assert_called_once_with(5001.0)

            calls = log.info.mock_calls
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0][1][1], "1h 23min")
            self._assert_isotime(calls[0][1][2], until)

    def test_wait_until(self):
        extr = extractor.find("generic:https://example.org/")
        until = time.time() + 5

        with patch("time.sleep") as sleep, patch.object(extr, "log") as log:
            extr.wait(until=until)

            calls = sleep.mock_calls
            self.assertEqual(len(calls), 1)
            self.assertAlmostEqual(calls[0][1][0], 6.0, places=0)

            calls = log.info.mock_calls
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0][1][1], "5 seconds")
            self._assert_isotime(calls[0][1][2], until)

    def test_wait_until_datetime(self):
        extr = extractor.find("generic:https://example.org/")
        until = dt.now() + dt.timedelta(seconds=5)
        until_local = dt.datetime.now() + dt.timedelta(seconds=5)

        if not until.microsecond:
            until = until.replace(microsecond=until_local.microsecond)

        with patch("time.sleep") as sleep, patch.object(extr, "log") as log:
            extr.wait(until=until)

            calls = sleep.mock_calls
            self.assertEqual(len(calls), 1)
            self.assertAlmostEqual(calls[0][1][0], 6.0, places=1)

            calls = log.info.mock_calls
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0][1][1], "5 seconds")
            self._assert_isotime(calls[0][1][2], until_local)

    def _assert_isotime(self, output, until):
        if until.__class__ is not dt.datetime:
            until = dt.datetime.fromtimestamp(until)
        o = self._isotime_to_seconds(output)
        u = self._isotime_to_seconds(until.time().isoformat()[:8])
        self.assertLessEqual(o-u, 1.0)

    def _isotime_to_seconds(self, isotime):
        parts = isotime.split(":")
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])


class TextExtractorCommonDateminmax(unittest.TestCase):

    def setUp(self):
        config.clear()

    tearDown = setUp

    def test_date_min_max_default(self):
        extr = extractor.find("generic:https://example.org/")

        dmin, dmax = extr._get_date_min_max()
        self.assertEqual(dmin, None)
        self.assertEqual(dmax, None)

        dmin, dmax = extr._get_date_min_max(..., -1)
        self.assertEqual(dmin, ...)
        self.assertEqual(dmax, -1)

    def test_date_min_max_timestamp(self):
        extr = extractor.find("generic:https://example.org/")
        config.setg("date-min", 1262304000)
        config.setg("date-max", 1262304000.123)

        dmin, dmax = extr._get_date_min_max()
        self.assertEqual(dmin, 1262304000)
        self.assertEqual(dmax, 1262304000.123)

    def test_date_min_max_iso(self):
        extr = extractor.find("generic:https://example.org/")
        config.setg("date-min", "2010-01-01")
        config.setg("date-max", "2010-01-01T00:01:03")

        dmin, dmax = extr._get_date_min_max()
        self.assertEqual(dmin, 1262304000)
        self.assertEqual(dmax, 1262304063)

    def test_date_min_max_iso_invalid(self):
        extr = extractor.find("generic:https://example.org/")
        config.setg("date-min", "2010-01-01")
        config.setg("date-max", "2010-01")

        with self.assertLogs() as log_info:
            dmin, dmax = extr._get_date_min_max()
        self.assertEqual(dmin, 1262304000)
        self.assertEqual(dmax, None)

        self.assertEqual(len(log_info.output), 1)
        self.assertEqual(
            log_info.output[0],
            "WARNING:generic:Unable to parse 'date-max': "
            "Invalid ISO 8601 date/time value '2010-01'")

    def test_date_min_max(self):
        extr = extractor.find("generic:https://example.org/")
        config.setg("date-min", "2010-01-01")
        config.setg("date-max", "2022-08-18")

        dmin, dmax = extr._get_date_min_max()
        self.assertEqual(dmin, 1262304000)
        self.assertEqual(dmax, 1660780800)

    def test_date_min_max_mix(self):
        extr = extractor.find("generic:https://example.org/")
        config.setg("date-min", "2010-01-01")
        config.setg("date-max", 1262304061)

        dmin, dmax = extr._get_date_min_max()
        self.assertEqual(dmin, 1262304000)
        self.assertEqual(dmax, 1262304061)


class TextExtractorOAuth(unittest.TestCase):

    def test_oauth1(self):
        for category in ("flickr", "smugmug", "tumblr"):
            extr = extractor.find(f"oauth:{category}")

            with patch.object(extr, "_oauth1_authorization_flow") as m:
                for msg in extr:
                    pass
                self.assertEqual(len(m.mock_calls), 1)

    def test_oauth2(self):
        for category in ("deviantart", "reddit"):
            extr = extractor.find(f"oauth:{category}")

            with patch.object(extr, "_oauth2_authorization_code_grant") as m:
                for msg in extr:
                    pass
                self.assertEqual(len(m.mock_calls), 1)

    def test_oauth2_mastodon(self):
        extr = extractor.find("oauth:mastodon:pawoo.net")

        with patch.object(extr, "_oauth2_authorization_code_grant") as m, \
                patch.object(extr, "_register") as r:
            for msg in extr:
                pass
            self.assertEqual(len(r.mock_calls), 0)
            self.assertEqual(len(m.mock_calls), 1)

    def test_oauth2_mastodon_unknown(self):
        extr = extractor.find("oauth:mastodon:example.com")

        with patch.object(extr, "_oauth2_authorization_code_grant") as m, \
                patch.object(extr, "_register") as r:
            r.__name__ = "_register"
            r.return_value = {
                "client-id"    : "foo",
                "client-secret": "bar",
            }

            extr.cache_update(r, "example.com", None)
            for msg in extr:
                pass

            self.assertEqual(len(r.mock_calls), 1)
            self.assertEqual(len(m.mock_calls), 1)


class TestImgbb(unittest.TestCase):
    _IMAGE_HTML = (
        "<html><head>\n"
        '<link title="In-Shot hosted at ImgBB — ImgBB">\n'
        '<meta property="og:url" content="https://ibb.co/dGFyRQm">\n'
        '<meta property="og:title" content="'
        'In-Shot-20220512-212334331 hosted at ImgBB">\n'
        '<meta property="og:image" content="https://i.ibb.co/'
        '9s6j7qZ/In-Shot-20220512-212334331.jpg">\n'
        '<meta property="og:image:width" content="1920">\n'
        '<meta property="og:image:height" content="1920">\n'
        "</head><body>\n"
        'Added to <a href="https://ibb.co/album/abc123">Test Album</a>\n'
        '<p>Uploaded <span title="2022-05-13 00:25:52">'
        "4 years ago</span></p>\n"
        '<a href="https://i.ibb.co/'
        '9s6j7qZ/In-Shot-20220512-212334331.jpg"'
        ' download="In-Shot-20220512-212334331.jpg"'
        ' class="btn btn-download default" rel="tooltip"'
        ' title="1920 x 1920 - JPG 1.7 MB"></a>\n'
        "<script>\n"
        'CHV.obj.resource={"id":"dGFyRQm","type":"image"};\n'
        'CHV.obj.image_viewer.image={"width":1920,"height":1920,'
        '"url":"https://i.ibb.co/'
        '9s6j7qZ/In-Shot-20220512-212334331.jpg"};\n'
        "</script>\n"
        "</body></html>\n"
    )

    class _Resp:
        def __init__(self, clen, ctype="image/jpeg", status=200):
            self.status_code = status
            self.headers = {
                "Content-Length": str(clen),
                "content-length": str(clen),
                "content-type": ctype,
                "Content-Type": ctype,
            }
            self.closed = False

        def close(self):
            self.closed = True

    def _image_extractor(self):
        from gallery_dl.extractor.imgbb import ImgbbImageExtractor
        extr = ImgbbImageExtractor.from_url("https://ibb.co/dGFyRQm")
        extr.initialize()
        return extr

    def test_parse_filesize(self):
        from gallery_dl.extractor.imgbb import _parse_filesize

        self.assertEqual(_parse_filesize("1.7 MB"), 1_700_000)
        self.assertEqual(
            _parse_filesize("1920 x 1920 - JPG 1.7 MB"), 1_700_000)
        self.assertEqual(_parse_filesize("182 B"), 182)
        self.assertEqual(_parse_filesize("45 KB"), 45_000)
        self.assertEqual(_parse_filesize("1.7 MiB"), 1_700_000)
        self.assertEqual(_parse_filesize(1_744_075), 1_744_075)
        self.assertEqual(_parse_filesize(""), 0)
        self.assertEqual(_parse_filesize(None), 0)
        self.assertEqual(_parse_filesize(
            "In-Shot-20220512-212334331 hosted at ImgBB — ImgBB"), 0)

    def test_cdn_truncated(self):
        from gallery_dl.extractor.imgbb import ImgbbExtractor

        trunc = ImgbbExtractor._cdn_truncated
        self.assertTrue(trunc(None, 819200, 1_700_000))
        self.assertFalse(trunc(None, 1_744_075, 1_700_000))
        self.assertFalse(trunc(None, 819200, 0))
        self.assertFalse(trunc(None, 0, 1_700_000))

    def test_image_page_size_from_download_button(self):
        extr = self._image_extractor()

        class _Page:
            text = self._IMAGE_HTML
        extr.request = lambda *a, **k: _Page()

        image, = extr.posts()
        self.assertEqual(image["id"], "dGFyRQm")
        self.assertEqual(image["title"], "In-Shot-20220512-212334331")
        self.assertEqual(
            image["url"],
            "https://i.ibb.co/9s6j7qZ/In-Shot-20220512-212334331.jpg")
        self.assertEqual(image["width"], 1920)
        self.assertEqual(image["height"], 1920)
        self.assertEqual(image["size"], 1_700_000)
        self.assertEqual(image["album"]["id"], "abc123")
        self.assertEqual(image["album"]["title"], "Test Album")

    def test_cdn_placeholder(self):
        from gallery_dl.extractor.imgbb import ImgbbExtractor

        url = "https://i.ibb.co/9s6j7qZ/file.jpg"
        ph = ImgbbExtractor._cdn_placeholder
        self.assertTrue(ph(None, self._Resp(1115, "image/png"), url))
        self.assertFalse(ph(None, self._Resp(819200, "image/jpeg"), url))
        self.assertFalse(ph(
            None, self._Resp(182, "image/png"),
            "https://i.ibb.co/1J4mTWzQ/test.png"))

    def test_cdn_failover_pins_complete_pop(self):
        from gallery_dl import http

        extr = self._image_extractor()
        extr._timeout = 5
        ips = {
            "i.ibb.co": ("207.174.26.219",),
            "ns1.ibb.co": ("51.75.213.70",),
            "ns2.ibb.co": ("23.237.219.162",),
            "ns3.ibb.co": ("207.174.26.219",),
        }
        extr._resolve_ipv4 = lambda name: ips.get(name, ())

        def fake_request(method, url, **kwargs):
            resolve = extr.session.curl_options.get(
                http.CurlOpt.RESOLVE) or ()
            ip = resolve[0].rsplit(":", 1)[-1] if resolve else ""
            if ip == "51.75.213.70":
                raise OSError("ssl")
            clen = 1744075 if ip == "23.237.219.162" else 819200
            return self._Resp(clen)

        extr.session.request = fake_request
        url = ("https://i.ibb.co/9s6j7qZ/"
               "In-Shot-20220512-212334331.jpg")
        result = extr._validate_cdn(
            self._Resp(819200), url, 1_700_000, set())
        self.assertEqual(result, url)
        pinned = extr.session.curl_options[http.CurlOpt.RESOLVE]
        self.assertIn("23.237.219.162", pinned[0])

    def test_cdn_complete_response_accepted(self):
        extr = self._image_extractor()
        url = ("https://i.ibb.co/9s6j7qZ/"
               "In-Shot-20220512-212334331.jpg")
        result = extr._validate_cdn(
            self._Resp(1_744_075), url, 1_700_000, set())
        self.assertTrue(result)

    def test_cdn_missing_size_skips_failover(self):
        extr = self._image_extractor()
        url = ("https://i.ibb.co/9s6j7qZ/"
               "In-Shot-20220512-212334331.jpg")
        result = extr._validate_cdn(
            self._Resp(819200), url, 0, set())
        self.assertTrue(result)

    def test_cdn_failover_exhausted_refuses_file(self):
        from gallery_dl import http

        extr = self._image_extractor()
        extr._timeout = 5
        ips = {
            "i.ibb.co": ("207.174.26.219",),
            "ns1.ibb.co": ("51.75.213.70",),
            "ns2.ibb.co": ("23.237.219.162",),
            "ns3.ibb.co": ("207.174.26.219",),
        }
        extr._resolve_ipv4 = lambda name: ips.get(name, ())
        extr.session.request = lambda *a, **k: self._Resp(819200)
        url = ("https://i.ibb.co/9s6j7qZ/"
               "In-Shot-20220512-212334331.jpg")
        with self.assertLogs(extr.log, "WARNING"):
            result = extr._validate_cdn(
                self._Resp(819200), url, 1_700_000, set())
        self.assertIs(result, False)
        self.assertFalse(
            extr.session.curl_options.get(http.CurlOpt.RESOLVE))


class TestGofile(unittest.TestCase):

    def setUp(self):
        config.clear()
        config.set(("extractor", "gofile"), "api-token", "test-token")

    def tearDown(self):
        config.clear()

    def _extractor(self, folder):
        from gallery_dl.extractor.gofile import GofileFolderExtractor
        extr = GofileFolderExtractor.from_url("https://gofile.io/d/GRl4Xn73")
        extr._get_content = lambda *a, **k: folder
        return extr

    def _files(self, children):
        folder = {
            "name": "Diara",
            "code": "GRl4Xn73",
            "canAccess": True,
            "type": "folder",
            "children": children,
        }
        files = []
        for msg in self._extractor(folder):
            if msg[0] == Message.Url:
                files.append(msg[2])
        return files

    def test_extension_from_mime(self):
        from gallery_dl.extractor.gofile import _extension_from_mime

        self.assertEqual(_extension_from_mime("image/jpeg"), "jpg")
        self.assertEqual(_extension_from_mime("image/jpeg; charset=binary"),
                         "jpg")
        self.assertEqual(_extension_from_mime("IMAGE/PNG"), "png")
        self.assertEqual(_extension_from_mime("image/webp"), "webp")
        self.assertEqual(_extension_from_mime("image/gif"), "gif")
        self.assertEqual(_extension_from_mime("image/svg+xml"), "svg")
        self.assertEqual(_extension_from_mime("image/xyzzy"), "xyzzy")
        self.assertEqual(_extension_from_mime("video/mp4"), "")
        self.assertEqual(_extension_from_mime("text/plain"), "")
        self.assertEqual(_extension_from_mime(""), "")
        self.assertEqual(_extension_from_mime(None), "")

    def test_extensionless_images_keep_mime_extension(self):
        files = self._files({
            "1": {
                "id": "1",
                "type": "file",
                "name": "Diara1.jpg",
                "mimetype": "image/jpeg",
                "link": "https://store.gofile.io/download/1",
            },
            "2": {
                "id": "2",
                "type": "file",
                "name": "Diara2",
                "mimetype": "image/jpeg",
                "link": "https://store.gofile.io/download/2",
            },
            "3": {
                "id": "3",
                "type": "file",
                "name": "Diara3",
                "mimetype": "image/png",
                "link": "https://store.gofile.io/download/3",
            },
        })
        by_name = {f["name"]: f for f in files}
        self.assertEqual(len(files), 3)

        self.assertEqual(by_name["Diara1.jpg"]["filename"], "Diara1")
        self.assertEqual(by_name["Diara1.jpg"]["extension"], "jpg")

        self.assertEqual(by_name["Diara2"]["filename"], "Diara2")
        self.assertEqual(by_name["Diara2"]["extension"], "jpg")

        self.assertEqual(by_name["Diara3"]["filename"], "Diara3")
        self.assertEqual(by_name["Diara3"]["extension"], "png")

    def test_extensionless_non_image_is_kept(self):
        files = self._files({
            "1": {
                "id": "1",
                "type": "file",
                "name": "notes",
                "mimetype": "text/plain",
                "link": "https://store.gofile.io/download/1",
            },
        })
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0]["filename"], "notes")
        self.assertEqual(files[0]["extension"], "")


if __name__ == "__main__":
    unittest.main()
