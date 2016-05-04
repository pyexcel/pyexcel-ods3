from pyexcel_io.io import get_data as read_data, isstream, store_data as write_data


__pyexcel_io_plugins__ = ['ods']


def save_data(afile, data, file_type=None, **keywords):
    if isstream(afile) and file_type is None:
        file_type = 'ods'
    write_data(afile, data, file_type=file_type, **keywords)


def get_data(afile, file_type=None, **keywords):
    if isstream(afile) and file_type is None:
        file_type = 'ods'
    return read_data(afile, file_type=file_type, **keywords)
