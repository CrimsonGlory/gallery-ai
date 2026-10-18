#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gallery_dl import update  # noqa E402


class TestUpdateChannels(unittest.TestCase):

    def test_repos(self):
        self.assertEqual(update.REPOS["stable"], "mikf/gallery-dl")
        self.assertEqual(update.REPOS["dev"], "CrimsonGlory/gallery-ai")
        self.assertEqual(update.REPOS["nightly"], "CrimsonGlory/gallery-ai")
        self.assertEqual(update.REPOS["master"], "CrimsonGlory/gallery-ai")

    def test_dev_binaries(self):
        binaries = update.BINARIES["dev"]
        self.assertEqual(binaries["linux"], "gallery-ai_linux")
        self.assertEqual(binaries["windows"], "gallery-ai_windows.exe")
        self.assertEqual(binaries["windows_x64"], "gallery-ai_windows.exe")
        self.assertEqual(binaries["macos"], "gallery-ai_macos")


if __name__ == "__main__":
    unittest.main()
