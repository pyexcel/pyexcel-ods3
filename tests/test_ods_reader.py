import os

from base import ODSCellTypes
from pyexcel_ods3.odsr import ODSBook
from pyexcel_ods3.odsw import ODSWriter


class TestODSReader(ODSCellTypes):
    def setUp(self):
        r = ODSBook()
        r.open(os.path.join("tests", "fixtures", "ods_formats.ods"))
        self.data = r.read_all()
        for key in self.data.keys():
            self.data[key] = list(self.data[key])
        r.close()


class TestODSWriter(ODSCellTypes):
    def setUp(self):
        r = ODSBook()
        r.open(
            os.path.join("tests", "fixtures", "ods_formats.ods"),
            skip_empty_rows=True,
        )
        self.data1 = r.read_all()
        self.testfile = "odswriter.ods"
        w = ODSWriter()
        w.open(self.testfile)
        w.write(self.data1)
        w.close()
        r2 = ODSBook()
        r2.open(self.testfile)
        self.data = r2.read_all()
        for key in self.data.keys():
            self.data[key] = list(self.data[key])

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
