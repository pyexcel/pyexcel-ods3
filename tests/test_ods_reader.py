import os

from base import ODSCellTypes
from pyexcel_io.reader import Reader
from pyexcel_ods3.odsw import ODSWriter


class TestODSReader(ODSCellTypes):
    def setUp(self):
        r = Reader("ods")
        r.open(os.path.join("tests", "fixtures", "ods_formats.ods"))
        self.data = r.read_all()
        for key in self.data.keys():
            self.data[key] = list(self.data[key])
        r.close()


class TestODSWriter(ODSCellTypes):
    def setUp(self):
        r = Reader("ods")
        r.open(
            os.path.join("tests", "fixtures", "ods_formats.ods"),
            skip_empty_rows=True,
        )
        self.data1 = r.read_all()
        r.close()
        self.testfile = "odswriter.ods"
        w = ODSWriter(self.testfile, "ods")
        w.write(self.data1)
        w.close()
        r.open(self.testfile)
        self.data = r.read_all()

        for key in self.data.keys():
            self.data[key] = list(self.data[key])
        r.close()

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
