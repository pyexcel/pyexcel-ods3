"""
    pyexcel_ods.odsbook
    ~~~~~~~~~~~~~~~~~~~

    ODS format plugin for pyexcel

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
import sys
import datetime
import ezodf
from collections import OrderedDict
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import BytesIO as StringIO


def float_value(value):
    ret = float(value)
    return ret


def date_value(value):
    tokens = value.split('-')
    year = int(tokens[0])
    month = int(tokens[1])
    day = int(tokens[2])
    ret = datetime.date(year, month, day)
    return ret


def time_value(value):
    hour = int(value[2:4])
    minute = int(value[5:7])
    second = int(value[8:10])
    ret = datetime.time(hour, minute, second)
    return ret


def boolean_value(value):
    return value


ODS_FORMAT_CONVERSION = {
    "float": float,
    "date": datetime.date,
    "time": datetime.time,
    "boolean": bool,
    "percentage": float,
    "currency": float
}


VALUE_CONVERTERS = {
    "float": float_value,
    "date": date_value,
    "time": time_value,
    "boolean": boolean_value,
    "percentage": float_value,
    "currency": float_value
}


VALUE_TOKEN = {
    "float": "value",
    "date": "date-value",
    "time": "time-value",
    "boolean": "boolean-value",
    "percentage": "value",
    "currency": "value"
}

ODS_WRITE_FORMAT_COVERSION = {
    float: "float",
    int: "float",
    str: "string",
    datetime.date: "date",
    datetime.time: "time",
    bool: "boolean"
}


if sys.version_info[0] < 3:
    ODS_WRITE_FORMAT_COVERSION[unicode] = "string"


class ODSBook:

    def __init__(self, filename, file_content=None, **keywords):
        """Load the file"""
        self.doc = ezodf.opendoc(filename, file_content)
        self.SHEETS = OrderedDict()
        self.sheet_names = []
        for sheet in self.doc.sheets:
            self.readSheet(sheet)

    def readSheet(self, sheet):
        """reads a sheet in the sheet dictionary, storing each sheet
        as an array (rows) of arrays (columns)"""
        table = []
        for row in range(sheet.nrows()):
            rows = []
            for column, cell in enumerate(sheet.row(row)):
                ret = self._read_cell(cell)
                rows.append(ret)
            # if row contained something
            table.append(rows)

        self.SHEETS[sheet.name] = table
        self.sheet_names.append(sheet.name)

    def _read_cell(self, cell):
        cell_type = cell.value_type
        ret = None
        if cell_type in ODS_FORMAT_CONVERSION:
            value = cell.value
            n_value = VALUE_CONVERTERS[cell_type](value)
            ret = n_value
        else:
            if cell.value is None:
                ret = ""
            else:
                ret = cell.value
        return ret

    def sheets(self):
        return self.SHEETS


class ODSSheetWriter:
    """
    ODS sheet writer
    """

    def __init__(self, book, name):
        self.doc = book
        if name:
            sheet_name = name
        else:
            sheet_name = "pyexcel_sheet1"
        self.sheet = ezodf.Sheet(sheet_name)
        self.current_row = 0

    def set_size(self, size):
        self.sheet.reset(size=size)

    def write_row(self, array):
        """
        write a row into the file
        """
        count = 0
        for cell in array:
            value_type = ODS_WRITE_FORMAT_COVERSION[type(cell)]
            if value_type == "time":
                cell = cell.strftime("PT%HH%MM%SS")
            self.sheet[self.current_row, count].set_value(
                cell,
                value_type=value_type)
            count += 1
        self.current_row += 1

    def write_array(self, table):
        rows = len(table)
        if rows > 0:
            columns = max(map(len, table))
        if columns == 0:
            return
        self.set_size((rows, columns))
        for row in table:
            self.write_row(row)

    def close(self):
        """
        This call writes file

        """
        self.doc.sheets += self.sheet


class ODSWriter:
    """
    open document spreadsheet writer

    """
    def __init__(self, filename):
        self.doc = ezodf.newdoc(doctype="ods", filename=filename)

    def create_sheet(self, name):
        """
        write a row into the file
        """
        return ODSSheetWriter(self.doc, name)

    def write(self, sheet_dicts):
        """Write a dictionary to a multi-sheet file

        Requirements for the dictionary is: key is the sheet name,
        its value must be two dimensional array
        """
        keys = sheet_dicts.keys()
        for name in keys:
            sheet = self.create_sheet(name)
            sheet.write_array(sheet_dicts[name])
            sheet.close()

    def close(self):
        """
        This call writes file

        """
        self.doc.save()
