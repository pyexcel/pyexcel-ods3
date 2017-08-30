#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
import psutil
import pyexcel as pe
from nose.tools import raises, eq_
from nose import SkipTest

IN_TRAVIS = 'TRAVIS' in os.environ


@raises(Exception)
def test_invalid_date():
    from pyexcel_ods3.ods import date_value
    value = "2015-08-"
    date_value(value)


@raises(Exception)
def test_fake_date_time_10():
    from pyexcel_ods3.ods import date_value
    date_value("1234567890")


@raises(Exception)
def test_fake_date_time_19():
    from pyexcel_ods3.ods import date_value
    date_value("1234567890123456789")


@raises(Exception)
def test_fake_date_time_20():
    from pyexcel_ods3.ods import date_value
    date_value("12345678901234567890")


def test_issue_10():
    test_file_name = "test_issue_10.ods"
    from pyexcel_ods3 import save_data
    content = {"test": [[1, 2]]}
    save_data(test_file_name, content)
    save_data(test_file_name, content)
    assert os.path.exists(test_file_name)
    assert os.path.exists(test_file_name + ".bak") is False
    os.unlink(test_file_name)


row_max = 2
col_max = 2


def data_gen():
    for row in range(row_max // 2):
        tmp = []
        for col in range(col_max):
            tmp.append("Row: %d Col: %d" % (row, col))
        for col in range(col_max):
            tmp.append((row + col))
        yield tmp


def test_issue_11():
    test_file = "test_file.ods"
    from pyexcel_ods3 import save_data
    save_data(test_file, {"generator": data_gen()})
    os.unlink(test_file)


def test_issue_8():
    from pyexcel_ods3 import get_data
    test_file = "12_day_as_time.ods"
    data = get_data(get_fixtures(test_file),
                    skip_empty_rows=True)
    eq_(data['Sheet1'][0][0].days, 12)


def test_issue_83_ods_file_handle():
    # this proves that odfpy
    # does not leave a file handle open at all
    proc = psutil.Process()
    test_file = get_fixtures("12_day_as_time.ods")
    open_files_l1 = proc.open_files()

    # start with a csv file
    data = pe.iget_array(file_name=test_file, library='pyexcel-ods3')
    open_files_l2 = proc.open_files()
    delta = len(open_files_l2) - len(open_files_l1)
    # cannot catch open file handle
    assert delta == 0

    # now the file handle get opened when we run through
    # the generator
    list(data)
    open_files_l3 = proc.open_files()
    delta = len(open_files_l3) - len(open_files_l1)
    # cannot catch open file handle
    assert delta == 0

    # free the fish
    pe.free_resources()
    open_files_l4 = proc.open_files()
    # this confirms that no more open file handle
    eq_(open_files_l1, open_files_l4)


def test_issue_23():
    if not IN_TRAVIS:
        raise SkipTest()
    pe.get_book(url="https://github.com/pyexcel/pyexcel-ods3/raw/master/tests/fixtures/multilineods.ods");  # flake8: noqa


def get_fixtures(filename):
    return os.path.join("tests", "fixtures", filename)
