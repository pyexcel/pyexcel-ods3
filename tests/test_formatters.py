import os
from unittest import TestCase
from textwrap import dedent

import pyexcel as pe


class TestAutoDetectInt(TestCase):
    def setUp(self):
        self.content = [[1, 2, 3.1]]
        self.test_file = "test_auto_detect_init.ods"
        pe.save_as(array=self.content, dest_file_name=self.test_file)

    def test_auto_detect_int(self):
        sheet = pe.get_sheet(file_name=self.test_file)
        expected = dedent("""
        pyexcel_sheet1:
        +---+---+-----+
        | 1 | 2 | 3.1 |
        +---+---+-----+""").strip()
        self.assertEqual(str(sheet), expected)

    def test_get_book_auto_detect_int(self):
        book = pe.get_book(file_name=self.test_file)
        expected = dedent("""
        pyexcel_sheet1:
        +---+---+-----+
        | 1 | 2 | 3.1 |
        +---+---+-----+""").strip()
        self.assertEqual(str(book), expected)

    def test_auto_detect_int_false(self):
        sheet = pe.get_sheet(file_name=self.test_file, auto_detect_int=False)
        expected = dedent("""
        pyexcel_sheet1:
        +-----+-----+-----+
        | 1.0 | 2.0 | 3.1 |
        +-----+-----+-----+""").strip()
        self.assertEqual(str(sheet), expected)

    def test_get_book_auto_detect_int_false(self):
        book = pe.get_book(file_name=self.test_file, auto_detect_int=False)
        expected = dedent("""
        pyexcel_sheet1:
        +-----+-----+-----+
        | 1.0 | 2.0 | 3.1 |
        +-----+-----+-----+""").strip()
        self.assertEqual(str(book), expected)

    def tearDown(self):
        os.unlink(self.test_file)
