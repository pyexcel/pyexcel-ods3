from io import BytesIO

from pyexcel_ods3 import get_data, save_data

import pytest


class Rows:
    def __iter__(self):
        yield [1, 2, 3]
        yield [4, 5, 6]


@pytest.mark.parametrize(
    "make_table",
    [
        lambda: iter([[1, 2, 3], [4, 5, 6]]),
        lambda: map(list, [(1, 2, 3), (4, 5, 6)]),
        lambda: zip([1, 4], [2, 5], [3, 6]),
        lambda: [iter([1, 2, 3]), iter([4, 5, 6])],
        lambda: (iter(row) for row in [[1, 2, 3], [4, 5, 6]]),
        Rows,
    ],
)
def test_write_single_pass_rows(make_table):
    stream = BytesIO()
    save_data(stream, {"data": make_table()})
    stream.seek(0)
    assert get_data(stream) == {"data": [[1, 2, 3], [4, 5, 6]]}


def test_write_empty_iterator():
    stream = BytesIO()
    save_data(stream, {"data": iter([])})
    stream.seek(0)
    assert get_data(stream) == {"data": []}
