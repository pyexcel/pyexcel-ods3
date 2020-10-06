"""
    pyexcel_ods3.odsw
    ~~~~~~~~~~~~~~~~~~~

    ods writer using ezodf

    :copyright: (c)  2015-2020 by Onni Software Ltd. & its contributors
    :license: New BSD License
"""
import types

import ezodf
import pyexcel_io.service as service
from pyexcel_io.constants import MAX_INTEGER
from pyexcel_io.exceptions import IntegerAccuracyLossError
from pyexcel_io.plugin_api import IWriter, ISheetWriter


class ODSSheetWriter(ISheetWriter):
    """
    ODS sheet writer
    """

    def __init__(self, ods_book, ods_sheet, sheet_name, **keywords):
        self._native_book = ods_book
        self._native_sheet = ezodf.Sheet(sheet_name)
        self.current_row = 0

    def _set_size(self, size):
        self._native_sheet.reset(size=size)

    def write_row(self, array):
        """
        write a row into the file
        """
        count = 0
        for cell in array:
            value_type = service.ODS_WRITE_FORMAT_COVERSION[type(cell)]
            if value_type == "time":
                cell = cell.strftime("PT%HH%MM%SS")
            elif value_type == "timedelta":
                hours = cell.days * 24 + cell.seconds // 3600
                minutes = (cell.seconds // 60) % 60
                seconds = cell.seconds % 60
                cell = "PT%02dH%02dM%02dS" % (hours, minutes, seconds)
                value_type = "time"
            elif value_type == "float":
                if cell > MAX_INTEGER:
                    raise IntegerAccuracyLossError("%s is too big" % cell)
            self._native_sheet[self.current_row, count].set_value(
                cell, value_type=value_type
            )
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
        self._set_size((rows, columns))
        for row in to_write_data:
            self.write_row(row)

    def close(self):
        """
        This call writes file

        """
        self._native_book.sheets += self._native_sheet


class ODSWriter(IWriter):
    """
    open document spreadsheet writer

    """

    def __init__(
        self, file_alike_object, file_type, skip_backup=True, **keywords
    ):
        """open a file for writing ods"""
        self._native_book = ezodf.newdoc(
            doctype=file_type, filename=file_alike_object
        )

        if skip_backup:
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
