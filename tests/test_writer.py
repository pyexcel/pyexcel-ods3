import os
import time

from base import PyexcelWriterBase, PyexcelHatWriterBase
from pyexcel_ods3 import get_data
from pyexcel_ods3.odsw import ODSWriter as Writer


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


def test_writing_100k_rows_stays_linear():
    # Regression test for the quadratic append() cost: writing a sheet
    # detached from the book and only attaching it on close() used to take
    # ~228s for 100000 rows, because attaching the fully populated sheet
    # made lxml reconcile the namespace declarations of every cell in one
    # pass. A fix keeping this linear should stay well under 10s even on
    # slow CI machines.
    test_file = "linear.ods"
    rows = [
        [i, i * 7, "verb", f"row {i}, a moderately long description string"]
        for i in range(100000)
    ]
    writer = Writer(test_file, "ods")
    t0 = time.perf_counter()
    writer.write({"Sheet1": rows})
    writer.close()
    elapsed = time.perf_counter() - t0

    content = get_data(test_file)
    written_rows = list(content["Sheet1"])
    assert written_rows[0] == rows[0]
    assert written_rows[-1] == rows[-1]

    os.unlink(test_file)

    assert elapsed < 10, (
        f"writing 100000 rows took {elapsed:.1f}s; "
        "this used to take ~228s due to quadratic namespace reconciliation"
    )


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
