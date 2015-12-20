import os
from pyexcel.ext import ods3
from base import ODSCellTypes


class TestODSReader(ODSCellTypes):
    def setUp(self):
        r = ods3.ODSBook(os.path.join("tests",
                                              "fixtures",
                                              "ods_formats.ods"))
        self.data = r.sheets()
        for key in self.data.keys():
            self.data[key] = list(self.data[key])


class TestODSWriter(ODSCellTypes):
    def setUp(self):
        r = ods3.ODSBook(os.path.join("tests",
                                             "fixtures",
                                             "ods_formats.ods"))
        self.data1 = r.sheets()
        self.testfile = "odswriter.ods"
        w = ods3.ODSWriter(self.testfile)
        w.write(self.data1)
        w.close()
        r2 = ods3.ODSBook(self.testfile)
        self.data = r2.sheets()
        for key in self.data.keys():
            self.data[key] = list(self.data[key])

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
