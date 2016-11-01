"""
    pyexcel_ods3.ods
    ~~~~~~~~~~~~~~~~~~~

    ODS format plugin for pyexcel

    :copyright: (c)  2015-2016 by Onni Software Ltd. & its contributors
    :license: New BSD License
"""
import sys
import math
import types

import ezodf
from pyexcel_io.book import BookReader, BookWriter
from pyexcel_io.sheet import SheetReader, SheetWriter

import pyexcel_ods3.converter as converter

PY27_BELOW = sys.version_info[0] == 2 and sys.version_info[1] < 7
if PY27_BELOW:
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict


class ODSSheet(SheetReader):
    """ODS sheet representation"""
    def __init__(self, sheet, auto_detect_int=True, **keywords):
        SheetReader.__init__(self, sheet, **keywords)
        self.auto_detect_int = auto_detect_int

    @property
    def name(self):
        return self.native_sheet.name

    def number_of_rows(self):
        """
        Number of rows in the xls sheet
        """
        return self.native_sheet.nrows()

    def number_of_columns(self):
        """
        Number of columns in the xls sheet
        """
        return self.native_sheet.ncols()

    def _cell_value(self, row, column):
        cell = self.native_sheet.get_cell((row, column))
        cell_type = cell.value_type
        ret = None
        if cell_type in converter.ODS_FORMAT_CONVERSION:
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
        rets = [sheet for sheet in self.native_book.sheets
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
        sheets = self.native_book.sheets
        length = len(sheets)
        if sheet_index < length:
            return self.read_sheet(sheets[sheet_index])
        else:
            raise IndexError("Index %d of out bound %d." % (sheet_index,
                                                            length))

    def read_all(self):
        """read all available sheets"""
        result = OrderedDict()
        for sheet in self.native_book.sheets:
            data_dict = self.read_sheet(sheet)
            result.update(data_dict)
        return result

    def read_sheet(self, native_sheet):
        sheet = ODSSheet(native_sheet, **self.keywords)
        return {native_sheet.name: sheet.to_array()}

    def _load_from_file(self):
        self.native_book = ezodf.opendoc(self.file_name)

    def _load_from_memory(self):
        self.native_book = ezodf.opendoc(self.file_stream)


class ODSSheetWriter(SheetWriter):
    """
    ODS sheet writer
    """
    def set_sheet_name(self, name):
        self.native_sheet = ezodf.Sheet(name)
        self.current_row = 0

    def set_size(self, size):
        self.native_sheet.reset(size=size)

    def write_row(self, array):
        """
        write a row into the file
        """
        count = 0
        for cell in array:
            value_type = converter.ODS_WRITE_FORMAT_COVERSION[type(cell)]
            if value_type == "time":
                cell = cell.strftime("PT%HH%MM%SS")
            elif value_type == "timedelta":
                hours = cell.days * 24 + cell.seconds // 3600
                minutes = (cell.seconds // 60) % 60
                seconds = cell.seconds % 60
                cell = "PT%02dH%02dM%02dS" % (hours, minutes, seconds)
                value_type = "time"
            self.native_sheet[self.current_row, count].set_value(
                cell,
                value_type=value_type)
            count += 1
        self.current_row += 1

    def write_array(self, table):
        to_write_data = table
        if isinstance(to_write_data, types.GeneratorType):
            to_write_data = list(table)
        rows = len(to_write_data)
        if rows < 1:
            return
        columns = max([len(row) for row in to_write_data])
        self.set_size((rows, columns))
        for row in to_write_data:
            self.write_row(row)

    def close(self):
        """
        This call writes file

        """
        self.native_book.sheets += self.native_sheet


class ODSWriter(BookWriter):
    """
    open document spreadsheet writer

    """
    def __init__(self):
        BookWriter.__init__(self)
        self.native_book = None

    def open(self, file_name, **keywords):
        """open a file for writing ods"""
        BookWriter.open(self, file_name, **keywords)
        self.native_book = ezodf.newdoc(doctype="ods",
                                        filename=self.file_alike_object)

        skip_backup_flag = self.keywords.get('skip_backup', True)
        if skip_backup_flag:
            self.native_book.backup = False

    def create_sheet(self, name):
        """
        write a row into the file
        """
        return ODSSheetWriter(self.native_book, None, name)

    def close(self):
        """
        This call writes file

        """
        self.native_book.save()


def is_integer_ok_for_xl_float(value):
    """check if a float had zero value in digits"""
    return value == math.floor(value)


_ods_registry = {
    "file_type": "ods",
    "reader": ODSBook,
    "writer": ODSWriter,
    "stream_type": "binary",
    "mime_type": "application/vnd.oasis.opendocument.spreadsheet",
    "library": "pyexcel-ods3"
}

exports = (_ods_registry, )
