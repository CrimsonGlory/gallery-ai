#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import unittest

SCRIPTS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
sys.path.insert(0, SCRIPTS)

import daily_test  # noqa: E402


LIVE_FAILED = """
https://example.com/a
F
https://example.com/b
E
https://example.com/c
s
======================================================================
FAIL: test_vk_photos_1 (__main__.TestExtractorResults)
https://vk.com/id398982326
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test/test_results.py", line 1, in test
AssertionError: '398982326' != ''
======================================================================
ERROR: test_hentaiimg_gallery_1 (__main__.TestExtractorResults)
https://ja.hentai-img-xxx.com/image/x/
----------------------------------------------------------------------
gallery_dl.exception.NotFoundError: Requested gallery could not be found

----------------------------------------------------------------------
Ran 3482 tests in 8849.464s

FAILED (failures=469, errors=500, skipped=299)
"""

UNIT_OK = """
test_load (test_cookies.TestCookies) ... ok
test_save (test_cookies.TestCookies) ... skipped 'no cookies'

----------------------------------------------------------------------
Ran 453 tests in 3.771s

OK (skipped=5)
"""


class TestParseUnittestLog(unittest.TestCase):

    def test_live_failed_counts_and_names(self):
        parsed = daily_test.parse_unittest_log(LIVE_FAILED)
        self.assertEqual(parsed["failed"], 469)
        self.assertEqual(parsed["errors"], 500)
        self.assertEqual(parsed["skipped"], 299)
        self.assertEqual(parsed["ran"], 3482)
        self.assertEqual(parsed["passed"], 3482 - 469 - 500 - 299)
        self.assertEqual(parsed["duration"], "8849.464s")
        self.assertIn("test_vk_photos_1", parsed["failed_tests"][0])
        self.assertIn("test_hentaiimg_gallery_1", parsed["error_tests"][0])
        self.assertEqual(len(parsed["all_failed"]), 2)

    def test_unit_ok_skipped(self):
        parsed = daily_test.parse_unittest_log(UNIT_OK)
        self.assertEqual(parsed["failed"], 0)
        self.assertEqual(parsed["errors"], 0)
        self.assertEqual(parsed["skipped"], 5)
        self.assertEqual(parsed["ran"], 453)
        self.assertEqual(parsed["passed"], 448)
        self.assertTrue(parsed["summary_line"].endswith("OK (skipped=5)")
                        or "OK (skipped=5)" in parsed["summary_line"])

    def test_excerpts_include_assertion(self):
        text = daily_test.format_excerpts(
            LIVE_FAILED, ["test_vk_photos_1 (__main__.TestExtractorResults)"],
            limit=4)
        self.assertIn("AssertionError", text)
        self.assertIn("test_vk_photos_1", text)

    def test_needs_grok(self):
        empty = daily_test.empty_result()
        self.assertFalse(daily_test.needs_grok(empty, empty))
        bad = daily_test.empty_result()
        bad["failed"] = 1
        bad["all_failed"] = ["test_x"]
        self.assertTrue(daily_test.needs_grok(empty, bad))


if __name__ == "__main__":
    unittest.main()
