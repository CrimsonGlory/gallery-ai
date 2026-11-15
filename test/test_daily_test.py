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


class TestPerFixGroups(unittest.TestCase):

    def test_group_key_extractor_and_matching_results(self):
        self.assertEqual(
            daily_test.group_key_for_path("gallery_dl/extractor/leakgallery.py"),
            "ie:leakgallery")
        self.assertEqual(
            daily_test.group_key_for_path("test/results/leakgallery.py"),
            "ie:leakgallery")

    def test_group_key_results_keeps_site_stem(self):
        self.assertEqual(
            daily_test.group_key_for_path("test/results/floofgens.py"),
            "ie:floofgens")
        self.assertEqual(
            daily_test.group_key_for_path("test/results/celebforum.py"),
            "ie:celebforum")

    def test_group_key_shared_extractor_and_library(self):
        self.assertEqual(
            daily_test.group_key_for_path("gallery_dl/extractor/common.py"),
            "core")
        self.assertEqual(
            daily_test.group_key_for_path("gallery_dl/http.py"),
            "lib:http")
        self.assertEqual(
            daily_test.group_key_for_path("test/test_http.py"),
            "lib:http")
        self.assertEqual(
            daily_test.group_key_for_path("docs/supportedsites.md"),
            "shared")

    def test_skip_downloads_and_tmp(self):
        self.assertFalse(daily_test.is_committable_path("tmp/daily-test/x.log"))
        self.assertFalse(daily_test.is_committable_path("image.png"))
        self.assertTrue(
            daily_test.is_committable_path("gallery_dl/extractor/leakgallery.py"))

    def test_results_import_stem(self):
        self.assertEqual(
            daily_test.results_import_stem("test/results/floofgens.py"), "e621")
        self.assertEqual(
            daily_test.results_import_stem("test/results/celebforum.py"),
            "xenforo")
        self.assertEqual(
            daily_test.results_import_stem("test/results/imagetwist.py"),
            "imagehosts")
        self.assertEqual(
            daily_test.results_import_stem("test/results/pawchive.py"),
            "pawchive")

    def test_coalesce_extractor_onto_unique_importer(self):
        groups = daily_test.group_paths([
            "gallery_dl/extractor/xenforo.py",
            "test/results/celebforum.py",
        ])
        self.assertEqual(set(groups), {"ie:celebforum"})
        self.assertCountEqual(
            groups["ie:celebforum"],
            ["gallery_dl/extractor/xenforo.py", "test/results/celebforum.py"],
        )

    def test_same_stem_extractor_and_results_stay_together(self):
        groups = daily_test.group_paths([
            "gallery_dl/extractor/leakgallery.py",
            "test/results/leakgallery.py",
        ])
        self.assertEqual(set(groups), {"ie:leakgallery"})

    def test_separate_sites_stay_separate(self):
        groups = daily_test.group_paths([
            "gallery_dl/extractor/leakgallery.py",
            "test/results/floofgens.py",
            "test/results/pawchive.py",
            "test/results/vanlifetrader.py",
        ])
        self.assertEqual(
            set(groups),
            {"ie:leakgallery", "ie:floofgens", "ie:pawchive",
             "ie:vanlifetrader"},
        )

    def test_shared_extractor_not_merged_when_two_importers(self):
        groups = daily_test.group_paths([
            "gallery_dl/extractor/e621.py",
            "test/results/floofgens.py",
            "test/results/blep.py",
        ])
        self.assertEqual(set(groups), {"ie:e621", "ie:floofgens", "ie:blep"})
        self.assertEqual(groups["ie:e621"], ["gallery_dl/extractor/e621.py"])

    def test_imagehosts_merges_when_only_one_results_module(self):
        groups = daily_test.group_paths([
            "gallery_dl/extractor/imagehosts.py",
            "test/results/imagetwist.py",
        ])
        self.assertEqual(set(groups), {"ie:imagetwist"})
        self.assertCountEqual(
            groups["ie:imagetwist"],
            ["gallery_dl/extractor/imagehosts.py",
             "test/results/imagetwist.py"],
        )

    def test_primary_groups_ignores_shared_docs(self):
        self.assertEqual(
            daily_test.primary_groups([
                "gallery_dl/extractor/leakgallery.py",
                "docs/supportedsites.md",
            ]),
            {"ie:leakgallery"},
        )

    def test_parse_and_match_fix_bullets(self):
        bullets = daily_test.parse_fix_bullets(
            "[daily-test] Fix 4 failing tests\n\n"
            "- leakgallery: load the APP_TOKEN on the first API call.\n"
            "- floofgens: treat post updated_at as an ISO datetime.\n")
        self.assertEqual(
            bullets["leakgallery"],
            "load the APP_TOKEN on the first API call.")
        name, body = daily_test.match_bullet("leakgallery", bullets)
        self.assertEqual(name, "leakgallery")
        self.assertIn("APP_TOKEN", body)

    def test_message_prefers_results_module_name(self):
        subject, body = daily_test.message_for_group(
            "ie:celebforum",
            ["gallery_dl/extractor/xenforo.py", "test/results/celebforum.py"],
            {"celebforum": "update the gone post URL."},
        )
        self.assertEqual(subject, "[daily-test] Fix celebforum")
        self.assertIn("gone post URL", body)

    def test_combined_subject_detection(self):
        self.assertTrue(
            daily_test._looks_combined_subject(
                "[daily-test] Fix 6 failing tests"))
        self.assertTrue(
            daily_test._looks_combined_subject(
                "[daily-test] Fix leakgallery, floofgens"))
        self.assertFalse(
            daily_test._looks_combined_subject(
                "[daily-test] Fix leakgallery"))

    def test_prompt_asks_for_per_fix_commits(self):
        prompt = daily_test.build_prompt(
            daily_test.PROMPT_TEMPLATE.read_text(encoding="utf-8"),
            today="2026-11-15",
            branch="master",
            head="abc",
            image="gallery-ai:latest",
            unit=daily_test.empty_result(),
            live=daily_test.empty_result(),
            excerpts="",
            log_tail="",
            do_commit=True,
            max_failures=10,
        )
        self.assertIn("one commit per independent fix", prompt.lower())
        self.assertIn("Never `[daily-test] Fix 2 failing tests`", prompt)
        self.assertIn("COMMITS:", prompt)
        self.assertNotIn("`[daily-test] Fix <N> failing tests`", prompt)


if __name__ == "__main__":
    unittest.main()
