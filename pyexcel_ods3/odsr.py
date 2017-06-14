"""
    pyexcel_ods3.odsr
    ~~~~~~~~~~~~~~~~~~~

    ods reader

    :copyright: (c)  2015-2017 by Onni Software Ltd. & its contributors
    :license: New BSD License
"""
import math

import ezodf

from pyexcel_io.sheet import SheetReader
from pyexcel_io.book import BookReader
from pyexcel_io._compact import OrderedDict

import pyexcel_ods3.converter as converter


class ODSSheet(SheetReader):
    """ODS sheet representation"""
    def __init__(self, sheet, auto_detect_int=True, **keywords):
        SheetReader.__init__(self, sheet, **keywords)
        self.auto_detect_int = auto_detect_int

    @property
    def name(self):
        return self._native_sheet.name

    def number_of_rows(self):
        """
        Number of rows in the xls sheet
        """
        return self._native_sheet.nrows()

    def number_of_columns(self):
        """
        Number of columns in the xls sheet
        """
        return self._native_sheet.ncols()

    def cell_value(self, row, column):
        cell = self._native_sheet.get_cell((row, column))
        cell_type = cell.value_type
        ret = None
        if cell_type == 'currency':
            cell_value = cell.value
            if is_integer_ok_for_xl_float(cell_value):
                cell_value = int(cell_value)

            ret = str(cell_value) + ' ' + cell.currency
        elif cell_type in converter.ODS_FORMAT_CONVERSION:
            value = cell.value
            n_value = converter.VALUE_CONVERTERS[cell_type](value)
            if cell_type == 'float' and self.auto_detect_int:
                if is_integer_ok_for_xl_float(n_value):
                    n_value = int(n_value)
            ret = n_value
        else:
            if cell.value is None:
                ret = ""
            else:
                ret = cell.value
        return ret


class ODSBook(BookReader):
    """read a ods book out"""
    def open(self, file_name, **keywords):
        """load ods from file"""
        BookReader.open(self, file_name, **keywords)
        self._load_from_file()

    def open_stream(self, file_stream, **keywords):
        """load ods from file stream"""
        BookReader.open_stream(self, file_stream, **keywords)
        self._load_from_memory()

    def read_sheet_by_name(self, sheet_name):
        """read a named sheet"""
        rets = [sheet for sheet in self._native_book.sheets
                if sheet.name == sheet_name]
        if len(rets) == 0:
            raise ValueError("%s cannot be found" % sheet_name)
        elif len(rets) == 1:
            return self.read_sheet(rets[0])
        else:
            raise ValueError(
                "More than 1 sheet named as %s are found" % sheet_name)

    def read_sheet_by_index(self, sheet_index):
        """read a sheet at an index"""
        sheets = self._native_book.sheets
        length = len(sheets)
        if sheet_index < length:
            return self.read_sheet(sheets[sheet_index])
        else:
            raise IndexError("Index %d of out bound %d." % (
                sheet_index, length))

    def read_all(self):
        """read all available sheets"""
        result = OrderedDict()
        for sheet in self._native_book.sheets:
            data_dict = self.read_sheet(sheet)
            result.update(data_dict)
        return result

    def read_sheet(self, native_sheet):
        sheet = ODSSheet(native_sheet, **self._keywords)
        return {native_sheet.name: sheet.to_array()}

    def close(self):
        self._native_book = None

    def _load_from_file(self):
        self._native_book = ezodf.opendoc(self._file_name)

    def _load_from_memory(self):
        self._native_book = ezodf.opendoc(self._file_stream)


def is_integer_ok_for_xl_float(value):
    """check if a float had zero value in digits"""
    return value == math.floor(value)
