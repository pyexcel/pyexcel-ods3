"""
pyexcel_ods3.odsr
~~~~~~~~~~~~~~~~~~~

ods reader

:copyright: (c)  2015-2022 by Onni Software Ltd. & its contributors
:license: New BSD License
"""

from io import BytesIO

import ezodf
import pyexcel_io.service as service
from pyexcel_io.plugin_api import ISheet, IReader, NamedContent


class ODSSheet(ISheet):
    """ODS sheet representation"""

    def __init__(self, sheet, auto_detect_int=True):
        self.auto_detect_int = auto_detect_int
        self.ods_sheet = sheet
        self._last_data_row = None  # lazily computed
        self._last_data_col = None  # lazily computed

    def _compute_data_bounds(self):
        """
        Scan all cells once to determine the last row and column that contain
        actual data (i.e. cells with a non-None value).

        ODS files produced by LibreOffice often contain rows whose
        ``table:number-rows-repeated`` attribute carries a very large value
        (e.g. 1 048 574) to apply formatting to the rest of the sheet.
        ezodf collapses each such block into a single row/column entry that
        still appears in ``nrows()`` / ``ncols()`` even though every cell is
        empty (value == None).  We therefore find the true data extent so
        that ghost rows and columns are silently ignored.

        Cells whose value is ``None`` are artifacts of ODS formatting.
        Cells whose value is ``""`` (empty string) are intentional user data
        and are preserved.
        """
        nrows = self.ods_sheet.nrows()
        ncols = self.ods_sheet.ncols()
        last_data_row = -1
        last_data_col = -1

        for row in range(nrows):
            for col in range(ncols):
                if self.ods_sheet.get_cell((row, col)).value is not None:
                    last_data_row = max(last_data_row, row)
                    last_data_col = max(last_data_col, col)

        self._last_data_row = last_data_row
        self._last_data_col = last_data_col

    def row_iterator(self):
        """Iterate over row indices, stopping after the last row with data."""
        if self._last_data_row is None:
            self._compute_data_bounds()
        return range(self._last_data_row + 1)

    def column_iterator(self, row):
        """Yield cell values up to the last column 
        that contains data in any row."""
        if self._last_data_col is None:
            self._compute_data_bounds()
        for column in range(self._last_data_col + 1):
            yield self.cell_value(row, column)

    def cell_value(self, row, column):
        cell = self.ods_sheet.get_cell((row, column))
        cell_type = cell.value_type
        ret = None
        if cell_type == "currency":
            cell_value = cell.value
            if service.has_no_digits_in_float(cell_value):
                cell_value = int(cell_value)

            if cell.currency is None:
                ret = str(cell_value)
            else:
                ret = str(cell_value) + " " + cell.currency
        elif cell_type in service.ODS_FORMAT_CONVERSION:
            value = cell.value
            n_value = service.VALUE_CONVERTERS[cell_type](value)
            if cell_type == "float" and self.auto_detect_int:
                if service.has_no_digits_in_float(n_value):
                    n_value = int(n_value)
            ret = n_value
        else:
            if cell.value is None:
                ret = ""
            else:
                ret = cell.value
        return ret


class ODSBook(IReader):
    def __init__(self, file_alike_object, file_type, **keywords):
        self.ods_book = ezodf.opendoc(file_alike_object)
        self._keywords = keywords
        self.content_array = [
            NamedContent(sheet.name, sheet) for sheet in self.ods_book.sheets
        ]

    def read_sheet(self, native_sheet_index):
        native_sheet = self.content_array[native_sheet_index].payload
        sheet = ODSSheet(native_sheet, **self._keywords)
        return sheet

    def close(self):
        self.ods_book = None


class ODSBookInContent(ODSBook):
    """
    Open ods as read only mode
    """

    def __init__(self, file_content, file_type, **keywords):
        io = BytesIO(file_content)
        super().__init__(io, file_type, **keywords)
