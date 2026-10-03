#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2026 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gallery_dl import http  # noqa: E402


class TestOmitNoneParams(unittest.TestCase):

    def test_dict_drops_none(self):
        self.assertEqual(
            http._omit_none_params({"type": None, "limit": 50, "q": "a"}),
            {"limit": 50, "q": "a"})

    def test_dict_filters_none_in_lists(self):
        self.assertEqual(
            http._omit_none_params({"lang": [None, "en"], "x": None}),
            {"lang": ["en"]})

    def test_list_of_pairs(self):
        self.assertEqual(
            http._omit_none_params([("a", 1), ("b", None), ("c", 3)]),
            [("a", 1), ("c", 3)])

    def test_passthrough(self):
        self.assertIsNone(http._omit_none_params(None))
        self.assertEqual(http._omit_none_params("a=1"), "a=1")


class TestSanitizeRequestKwargs(unittest.TestCase):

    def test_drops_none_params_and_headers(self):
        kwargs = http._sanitize_request_kwargs({
            "params": {"type": None, "limit": 10},
            "headers": {"Accept": "application/json", "Cookie": None},
            "data": {"token": "x", "unused": None},
        })
        self.assertEqual(kwargs["params"], {"limit": 10})
        self.assertEqual(kwargs["headers"], {"Accept": "application/json"})
        self.assertEqual(kwargs["data"], {"token": "x"})

    def test_empty_params_removed(self):
        kwargs = http._sanitize_request_kwargs({"params": {"type": None}})
        self.assertNotIn("params", kwargs)


class TestResponseContextManager(unittest.TestCase):

    def test_response_is_context_manager(self):
        self.assertTrue(callable(getattr(http.Response, "__enter__", None)))
        self.assertTrue(callable(getattr(http.Response, "__exit__", None)))


if __name__ == "__main__":
    unittest.main()
