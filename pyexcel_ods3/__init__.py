"""
    pyexcel_ods3
    ~~~~~~~~~~~~~~~~~~~

    The lower level ods file format handler using ezodf

    :copyright: (c) 2015-2017 by Onni Software Ltd & its contributors
    :license: New BSD License
"""

# flake8: noqa
from pyexcel_io.io import get_data as read_data
from pyexcel_io.io import isstream
from pyexcel_io.io import store_data as write_data

# this line has to be place above all else
# because of dynamic import
from pyexcel_io.plugins import IOPluginInfoChain, IOPluginInfoChainV2

__FILE_TYPE__ = "ods"
IOPluginInfoChainV2(__name__).add_a_reader(
    relative_plugin_class_path="odsr.ODSBook",
    locations=["file", "memory"],
    file_types=[__FILE_TYPE__],
    stream_type="binary",
).add_a_reader(
    relative_plugin_class_path="odsr.ODSBookInContent",
    locations=["content"],
    file_types=[__FILE_TYPE__],
    stream_type="binary",
).add_a_writer(
    relative_plugin_class_path="odsw.ODSWriter",
    locations=["file", "memory"],
    file_types=[__FILE_TYPE__],
    stream_type="binary",
)


def save_data(afile, data, file_type=None, **keywords):
    """standalone module function for writing module supported file type"""
    if isstream(afile) and file_type is None:
        file_type = __FILE_TYPE__
    write_data(afile, data, file_type=file_type, **keywords)


def get_data(afile, file_type=None, **keywords):
    """standalone module function for reading module supported file type"""
    if isstream(afile) and file_type is None:
        file_type = __FILE_TYPE__
    return read_data(afile, file_type=file_type, **keywords)
