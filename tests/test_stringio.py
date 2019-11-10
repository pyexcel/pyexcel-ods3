import os

import pyexcel
from base import create_sample_file1

from nose.tools import eq_


class TestStringIO:
    def test_ods_stringio(self):
        testfile = "cute.ods"
        create_sample_file1(testfile)
        with open(testfile, "rb") as f:
            content = f.read()
            r = pyexcel.get_sheet(
                file_type="ods", file_content=content, library="pyexcel-ods3"
            )
            result = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", 1.1, 1]
            actual = list(r.enumerate())
            eq_(result, actual)
        if os.path.exists(testfile):
            os.unlink(testfile)

    def test_ods_output_stringio(self):
        data = [[1, 2, 3], [4, 5, 6]]
        io = pyexcel.save_as(dest_file_type="ods", array=data)
        r = pyexcel.get_sheet(
            file_type="ods", file_content=io.getvalue(), library="pyexcel-ods3"
        )
        result = [1, 2, 3, 4, 5, 6]
        actual = list(r.enumerate())
        eq_(result, actual)
