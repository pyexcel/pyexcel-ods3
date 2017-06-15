"""
    pyexcel_ods3.odsw
    ~~~~~~~~~~~~~~~~~~~

    ods writer using ezodf

    :copyright: (c)  2015-2017 by Onni Software Ltd. & its contributors
    :license: New BSD License
"""
import types

import ezodf

from pyexcel_io.sheet import SheetWriter
from pyexcel_io.book import BookWriter

import pyexcel_ods3.converter as converter


class ODSSheetWriter(SheetWriter):
    """
    ODS sheet writer
    """
    def set_sheet_name(self, name):
        self._native_sheet = ezodf.Sheet(name)
        self.current_row = 0

    def set_size(self, size):
        self._native_sheet.reset(size=size)

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
            self._native_sheet[self.current_row, count].set_value(
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
        self._native_book.sheets += self._native_sheet


class ODSWriter(BookWriter):
    """
    open document spreadsheet writer

    """
    def __init__(self):
        BookWriter.__init__(self)
        self._native_book = None

    def open(self, file_name, **keywords):
        """open a file for writing ods"""
        BookWriter.open(self, file_name, **keywords)
        self._native_book = ezodf.newdoc(
            doctype="ods", filename=self._file_alike_object)

        skip_backup_flag = self._keywords.get('skip_backup', True)
        if skip_backup_flag:
            self._native_book.backup = False

    def create_sheet(self, name):
        """
        write a row into the file
        """
        return ODSSheetWriter(self._native_book, None, name)

    def close(self):
        """
        This call writes file

        """
        self._native_book.save()
        self._native_book = None
