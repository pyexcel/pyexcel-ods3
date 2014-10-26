import os
import pyexcel
from pyexcel.ext import ods3
import sys
if sys.version_info[0]< 2:
    from StringIO import StringIO
else:
    from io import BytesIO as StringIO
from base import create_sample_file1


class TestStringIO:

    def test_ods_stringio(self):
        odsfile = "cute.ods"
        create_sample_file1(odsfile)
        with open(odsfile, "rb") as f:
            content = f.read()
            try:
                r = pyexcel.Reader(("ods", content))
                assert 1==2
            except NotImplementedError:
                assert 1==1
        if os.path.exists(odsfile):
            os.unlink(odsfile)


    def test_xls_output_stringio(self):
        data = [
            [1, 2, 3],
            [4, 5, 6]
        ]
        io = StringIO()
        try:
            w = pyexcel.Writer(("ods",io))
            assert 1==2
        except NotImplementedError:
            assert 1==1
