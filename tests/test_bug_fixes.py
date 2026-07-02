import os

import psutil
import pyexcel as pe
from pyexcel_io.exceptions import IntegerAccuracyLossError

import pytest

IN_TRAVIS = "TRAVIS" in os.environ


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
    data = get_data(get_fixtures(test_file), skip_empty_rows=True)
    assert data["Sheet1"][0][0].days == 12


def test_issue_83_ods_file_handle():
    # this proves that odfpy
    # does not leave a file handle open at all
    proc = psutil.Process()
    test_file = get_fixtures("12_day_as_time.ods")
    open_files_l1 = proc.open_files()

    # start with a csv file
    data = pe.iget_array(file_name=test_file, library="pyexcel-ods3")
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
    assert open_files_l1 == open_files_l4


def test_issue_23():
    if not IN_TRAVIS:
        pytest.skip()
    url = (
        "https://github.com/pyexcel/pyexcel-ods3/"
        + "raw/master/tests/fixtures/multilineods.ods"
    )
    pe.get_book(url=url)


def test_issue_30():
    test_file = "issue_30.ods"
    sheet = pe.Sheet()
    sheet[0, 0] = 999999999999999
    sheet.save_as(test_file)
    sheet2 = pe.get_sheet(file_name=test_file)
    assert sheet[0, 0] == sheet2[0, 0]
    os.unlink(test_file)


def test_issue_30_precision_loss():
    test_file = "issue_30_2.ods"
    sheet = pe.Sheet()
    sheet[0, 0] = 9999999999999999
    with pytest.raises(IntegerAccuracyLossError):
        sheet.save_as(test_file)


def test_issue_36():
    from pyexcel_ods3 import get_data

    test_file = "currency_without_currency.ods"
    data = get_data(get_fixtures(test_file))
    assert data["Sheet1"][6][0] == '1.75"'
    assert data["Sheet1"][6][5] == "95"
    assert data["Sheet1"][6][6] == 25


def test_issue_24_ghost_rows():
    """Ghost rows caused by ODS styling 
    (number-rows-repeated) should be ignored."""
    from pyexcel_ods3 import get_data

    data = get_data(get_fixtures("issue_24_ghost_rows.ods"))
    assert data["Sheet1"] == [["A1", "B1"], ["A2", "B2"]]


def test_issue_24_ghost_rows_and_cols():
    """Ghost rows and columns caused by 
    whole-row/column ODS styling should be ignored."""
    from pyexcel_ods3 import get_data

    data = get_data(get_fixtures("issue_24_ghost_rows_and_cols.ods"))
    assert data["Sheet1"] == [["A1", "B1"], ["A2", "B2"]]

    data_keep = get_data(
        get_fixtures("issue_24_ghost_rows_and_cols.ods"),
        keep_trailing_empty_cells=True,
    )
    assert data_keep["Sheet1"] == [["A1", "B1"], ["A2", "B2"]]


def get_fixtures(filename):
    return os.path.join("tests", "fixtures", filename)
