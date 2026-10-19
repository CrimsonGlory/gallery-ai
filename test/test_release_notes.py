#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import unittest

SCRIPTS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
sys.path.insert(0, SCRIPTS)

import release_notes  # noqa: E402


LOG = """\
41ac8cbe4\tName PyInstaller binaries gallery-ai and target glibc 2.17
2a1187af7\t[upstream] Merge gallery-dl master (61971e01)
bca0b1245\t[upstream] Merge gallery-dl master (fae9305a)
07a3abcd4\tAdd daily GitHub release workflow and release.sh
"""

OLD_CHANGELOG = """# Changelog

## 1.32.13 - 2026-09-19
### Extractors
- old item
## 1.32.12 - 2026-09-12
"""

NEW_CHANGELOG = """# Changelog

## 1.32.17 - 2026-10-17
### Extractors
- new item
## 1.32.16 - 2026-10-09
## 1.32.15 - 2026-10-03
## 1.32.14 - 2026-09-27
## 1.32.13 - 2026-09-19
### Extractors
- old item
## 1.32.12 - 2026-09-12
"""


class TestReleaseNotes(unittest.TestCase):

    def test_parse_and_filter_upstream_merges(self):
        entries = release_notes.parse_first_parent_log(LOG)
        self.assertEqual(len(entries), 4)
        self.assertEqual(release_notes.upstream_merge_count(entries), 2)
        commits = release_notes.fork_commits(entries)
        self.assertEqual(
            [subject for _, subject in commits],
            [
                "Name PyInstaller binaries gallery-ai and target glibc 2.17",
                "Add daily GitHub release workflow and release.sh",
            ],
        )

    def test_new_changelog_headings_keep_order(self):
        added = release_notes.new_changelog_headings(OLD_CHANGELOG, NEW_CHANGELOG)
        self.assertEqual(added, [
            "1.32.17 - 2026-10-17",
            "1.32.16 - 2026-10-09",
            "1.32.15 - 2026-10-03",
            "1.32.14 - 2026-09-27",
        ])

    def test_notes_are_this_release_only(self):
        entries = release_notes.parse_first_parent_log(LOG)
        text = release_notes.format_notes(
            tag="2026.10.18.061406",
            sha="41ac8cbe4fbff5d7c8e736316f7af84ad742abd1",
            repo="CrimsonGlory/gallery-ai",
            commits=release_notes.fork_commits(entries)[:1],
            changelog_versions=release_notes.new_changelog_headings(
                OLD_CHANGELOG, NEW_CHANGELOG),
            prev_tag="2026.10.18.034716",
            upstream_merges=2,
        )
        self.assertIn("### Changes since 2026.10.18.034716", text)
        self.assertIn(
            "- Name PyInstaller binaries gallery-ai and target glibc 2.17 (`41ac8cbe4`)",
            text,
        )
        self.assertIn("- 1.32.17 - 2026-10-17", text)
        self.assertIn("- 1.32.14 - 2026-09-27", text)
        self.assertNotIn("Add daily GitHub release workflow", text)
        self.assertNotIn("[upstream] Merge gallery-dl master", text)
        self.assertNotIn("1.32.13 - 2026-09-19", text)
        self.assertNotIn("old item", text)
        self.assertIn(
            "https://github.com/CrimsonGlory/gallery-ai/compare/"
            "2026.10.18.034716...2026.10.18.061406",
            text,
        )

    def test_upstream_only_summarizes_merges(self):
        text = release_notes.format_notes(
            tag="2026.10.19.000000",
            sha="abc",
            repo="CrimsonGlory/gallery-ai",
            commits=[],
            changelog_versions=[],
            prev_tag="2026.10.18.061406",
            upstream_merges=3,
        )
        self.assertIn("Merged gallery-dl master (3 commits).", text)
        self.assertNotIn("No listed changes.", text)

    def test_no_previous_changelog_does_not_list_all_versions(self):
        added = release_notes.new_changelog_headings("", NEW_CHANGELOG)
        self.assertEqual(len(added), 6)
        text = release_notes.format_notes(
            tag="2026.10.18.034716",
            sha="07a3abcd",
            repo="CrimsonGlory/gallery-ai",
            commits=[],
            changelog_versions=[],
            prev_tag=None,
            initial=True,
            based_on="1.32.13",
        )
        self.assertIn("Initial gallery-ai release (gallery-dl 1.32.13).", text)
        self.assertNotIn("Merged gallery-dl:", text)
        self.assertNotIn("1.32.12", text)

    def test_initial_release_does_not_dump_history(self):
        text = release_notes.format_notes(
            tag="2026.10.18.034716",
            sha="07a3abcd4bad5d60faecb0c0713eec97001b2b3c",
            repo="CrimsonGlory/gallery-ai",
            commits=[
                ("07a3abcd4", "Add daily GitHub release workflow and release.sh"),
            ],
            changelog_versions=[],
            prev_tag=None,
            files=release_notes.LEGACY_FILES,
            binary_name="gallery-dl",
            initial=True,
            based_on="1.32.13",
        )
        self.assertIn("gallery-ai 2026.10.18.034716", text)
        self.assertIn("Initial gallery-ai release (gallery-dl 1.32.13).", text)
        self.assertIn("`gallery-dl -U`", text)
        self.assertIn("Add daily GitHub release workflow and release.sh", text)
        self.assertNotIn("### Changes since", text)
        self.assertNotIn("/compare/", text)


if __name__ == "__main__":
    unittest.main()
