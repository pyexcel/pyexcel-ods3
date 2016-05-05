"""
    pyexcel_ods3
    ~~~~~~~~~~~~~~~~~~~

    The lower level ods file format handler using ezodf

    :copyright: (c) 2015-2016 by Onni Software Ltd & its contributors
    :license: New BSD License
"""
__pyexcel_io_plugins__ = ['ods']

from pyexcel_io.io import get_data as read_data, isstream, store_data as write_data


def save_data(afile, data, file_type=None, **keywords):
    if isstream(afile) and file_type is None:
        file_type = 'ods'
    write_data(afile, data, file_type=file_type, **keywords)


def get_data(afile, file_type=None, **keywords):
    if isstream(afile) and file_type is None:
        file_type = 'ods'
    return read_data(afile, file_type=file_type, **keywords)
