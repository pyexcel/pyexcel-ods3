from pyexcel.io import READERS
from pyexcel.io import WRITERS
from .odsbook import ODSBook, ODSWriter

READERS["ods"] = ODSBook
WRITERS["ods"] = ODSWriter
