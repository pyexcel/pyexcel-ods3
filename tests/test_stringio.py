import os
from unittest import TestCase
import pyexcel
from base import create_sample_file1


class TestStringIO(TestCase):

    def test_ods_stringio(self):
        odsfile = "cute.ods"
        create_sample_file1(odsfile)
        with open(odsfile, "rb") as f:
            content = f.read()
            r = pyexcel.get_sheet(file_type="ods", file_content=content)
            result = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 1.1, 1]
            actual = list(r.enumerate())
            self.assertEqual(result, actual)
        if os.path.exists(odsfile):
            os.unlink(odsfile)

    def test_xls_output_stringio(self):
        data = [
            [1, 2, 3],
            [4, 5, 6]
        ]
        io = pyexcel.save_as(dest_file_type='ods', array=data)
        r = pyexcel.get_sheet(file_type="ods", file_content=io.getvalue())
        result = [1, 2, 3, 4, 5, 6]
        actual = list(r.enumerate())
        self.assertEqual(result, actual)
