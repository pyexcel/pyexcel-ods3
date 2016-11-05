#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
from nose.tools import raises


def test_date_util_parse():
    from pyexcel_ods3.converter import date_value
    value = "2015-08-17T19:20:00"
    d = date_value(value)
    assert d.strftime("%Y-%m-%dT%H:%M:%S") == "2015-08-17T19:20:00"
    value = "2015-08-17"
    d = date_value(value)
    assert d.strftime("%Y-%m-%d") == "2015-08-17"
    value = "2015-08-17T19:20:59.999999"
    d = date_value(value)
    assert d.strftime("%Y-%m-%dT%H:%M:%S") == "2015-08-17T19:20:59"
    value = "2015-08-17T19:20:59.99999"
    d = date_value(value)
    assert d.strftime("%Y-%m-%dT%H:%M:%S") == "2015-08-17T19:20:59"
    value = "2015-08-17T19:20:59.999999999999999"
    d = date_value(value)
    assert d.strftime("%Y-%m-%dT%H:%M:%S") == "2015-08-17T19:20:59"


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
