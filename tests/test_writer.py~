import os
import pyexcel
import pyexcel_ods
from base import PyexcelWriterBase, PyexcelHatWriterBase


class TestODSnCSVWriter(PyexcelWriterBase):
    def setUp(self):
        self.testfile="test.ods"
        self.testfile2="test.csv"

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
        if os.path.exists(self.testfile2):
            os.unlink(self.testfile2)


class TestODSHatWriter(PyexcelHatWriterBase):
    def setUp(self):
        self.testfile="test.ods"

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


