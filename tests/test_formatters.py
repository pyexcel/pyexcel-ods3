import os
from textwrap import dedent

import pyexcel as pe

from nose.tools import eq_


class TestAutoDetectInt:
    def setUp(self):
        self.content = [[1, 2, 3.1]]
        self.test_file = "test_auto_detect_init.ods"
        pe.save_as(array=self.content, dest_file_name=self.test_file)

    def test_auto_detect_int(self):
        sheet = pe.get_sheet(file_name=self.test_file, library="pyexcel-ods3")
        expected = dedent(
            """
        pyexcel_sheet1:
        +---+---+-----+
        | 1 | 2 | 3.1 |
        +---+---+-----+"""
        ).strip()
        eq_(str(sheet), expected)

    def test_get_book_auto_detect_int(self):
        book = pe.get_book(file_name=self.test_file, library="pyexcel-ods3")
        expected = dedent(
            """
        pyexcel_sheet1:
        +---+---+-----+
        | 1 | 2 | 3.1 |
        +---+---+-----+"""
        ).strip()
        eq_(str(book), expected)

    def test_auto_detect_int_false(self):
        sheet = pe.get_sheet(
            file_name=self.test_file,
            auto_detect_int=False,
            library="pyexcel-ods3",
        )
        expected = dedent(
            """
        pyexcel_sheet1:
        +-----+-----+-----+
        | 1.0 | 2.0 | 3.1 |
        +-----+-----+-----+"""
        ).strip()
        eq_(str(sheet), expected)

    def test_get_book_auto_detect_int_false(self):
        book = pe.get_book(
            file_name=self.test_file,
            auto_detect_int=False,
            library="pyexcel-ods3",
        )
        expected = dedent(
            """
        pyexcel_sheet1:
        +-----+-----+-----+
        | 1.0 | 2.0 | 3.1 |
        +-----+-----+-----+"""
        ).strip()
        eq_(str(book), expected)

    def tearDown(self):
        os.unlink(self.test_file)
