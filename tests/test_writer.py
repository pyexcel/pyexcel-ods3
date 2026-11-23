import os
from io import BytesIO

import ezodf
from base import PyexcelWriterBase, PyexcelHatWriterBase
from pyexcel_ods3 import get_data, save_data
from pyexcel_ods3.odsw import ODSWriter as Writer


def test_write_blank_cells():
    output = BytesIO()
    save_data(output, {"Data": [[None, "", None, 0, False, "end", None]]})

    sheet = ezodf.opendoc(BytesIO(output.getvalue())).sheets[0]
    assert [(cell.value_type, cell.value) for cell in sheet.row(0)] == [
        (None, None),
        ("string", ""),
        (None, None),
        ("float", 0),
        ("boolean", False),
        ("string", "end"),
        (None, None),
    ]


def test_write_empty_sheets():
    output = BytesIO()
    save_data(output, {"Empty": [], "Empty rows": [[], []], "Data": [[1]]})

    assert get_data(BytesIO(output.getvalue())) == {
        "Empty": [],
        "Empty rows": [],
        "Data": [[1]],
    }


class TestNativeODSWriter:
    def test_write_book(self):
        self.content = {
            "Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]],
            "Sheet2": [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]],
            "Sheet3": [["X", "Y", "Z"], [1, 4, 7], [2, 5, 8], [3, 6, 9]],
        }
        self.testfile = "writer.ods"
        writer = Writer(self.testfile, "ods")
        writer.write(self.content)
        writer.close()
        content = get_data(self.testfile)
        for key in content.keys():
            content[key] = list(content[key])
        assert content == self.content

    def teardown_method(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestodsnCSVWriter(PyexcelWriterBase):
    def setup_method(self):
        self.testfile = "test.ods"
        self.testfile2 = "test.csv"

    def teardown_method(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
        if os.path.exists(self.testfile2):
            os.unlink(self.testfile2)


class TestodsHatWriter(PyexcelHatWriterBase):
    def setup_method(self):
        self.testfile = "test.ods"

    def teardown_method(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


def test_pr_28():
    from datetime import datetime

    test_file = "pr28.ods"
    test = {"shee1": [[datetime(2022, 1, 30, 15, 45, 45)]]}
    writer = Writer(test_file, "ods")
    writer.write(test)
    writer.close()

    content = get_data(test_file)
    for key in content.keys():
        content[key] = list(content[key])
    assert content == {"shee1": [[datetime(2022, 1, 30, 15, 45, 45)]]}

    os.unlink(test_file)
