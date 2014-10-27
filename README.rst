============
pyexcel-ods3
============

.. image:: https://api.travis-ci.org/chfw/pyexcel-ods3.png
    :target: http://travis-ci.org/chfw/pyexcel-ods3

.. image:: https://pypip.in/d/pyexcel-ods3/badge.png
    :target: https://pypi.python.org/pypi/pyexcel-ods3

.. image:: https://pypip.in/py_versions/pyexcel-ods3/badge.png
    :target: https://pypi.python.org/pypi/pyexcel-ods3

.. image:: https://pypip.in/implementation/pyexcel-ods3/badge.png
    :target: https://pypi.python.org/pypi/pyexcel-ods3


**pyexcel-ods3** is a tiny wrapper library to read, manipulate and write data in ods fromat using python 2.7, python 3.3 and python 3.4. You are likely to use `pyexcel <https://github.com/chfw/pyexcel>`_ together with this library. `pyexcel-ods <https://github.com/chfw/pyexcel-ods>`_ is a sister library that does the same thing but supports python 2.6 and has no dependency on lxml.


Installation
============

You can install it via pip::

    $ pip install git+https://github.com/chfw/ezodf.git
    $ pip install pyexcel-ods3

or clone it and install it::

    $ pip install git+https://github.com/chfw/ezodf.git
    $ pip install git+http://github.com/chfw/pyexcel-ods3.git
    $ cd pyexcel-ods3
    $ python setup.py install


The installation of `lxml` will be tricky on Widnows platform. It is recommended that you download a lxml's own windows installer instead of using pip.

Constaint
==========

**pyexcel-ods3 v0.0.1** does not support memory file. But new versions(0.0.2+) supports meomory file unless `my version of ezodf <https://github.com/chfw/ezodf>`_ is installed

Usage
=====

As a standalone library
------------------------

Read from an ods file
**********************

Here's the sample code::

    from pyexcel_ods3 import ODSBook
    import json

    book = ODSBook("your_file.ods")
    # book.sheets() returns a dictionary of all sheet content
    #   the keys represents sheet names
    #   the values are two dimensional array
    print(book.sheets())

Write to an ods file
*********************

Here's the sample code to write a dictionary to an ods file::

    from pyexcel_ods3 import ODSWriter

    data = {
        "Sheet 1": [[1, 2, 3], [4, 5, 6]],
        "Sheet 2": [["row 1", "row 2", "row 3"]]
    }
    writer = ODSWriter("your_file.ods")
    writer.write(data)
    writer.close()

Read from an ods from memory
*****************************

Here's the sample code::

    from pyexcel_ods3 import ODSBook

    # This is just an illustration
    # In reality, you might deal with ods file upload
    # where you will read from requests.FILES['YOUR_ODS_FILE']
    odsfile = "example.ods"
    with open(odsfile, "rb") as f:
        content = f.read()
        book = ODSBook(None, content)
        print(book.sheets())


Write an ods to memory
**********************

Here's the sample code to write a dictionary to an ods file::

    from pyexcel_ods3 import ODSWriter
    from StringIO import StringIO

    data = {
        "Sheet 1": [[1, 2, 3], [4, 5, 6]],
        "Sheet 2": [["row 1", "row 2", "row 3"]]
    }
    io = StringIO()
    writer = ODSWriter(io)
    writer.write(data)
    writer.close()
    # do something witht the io
    # In reality, you might give it to your http response
    # object for downloading

As a pyexcel plugin
--------------------

Import it in your file to enable this plugin::

    from pyexcel.ext import ods3

Please note only pyexcel version 0.0.4+ support this.

Reading from an ods file
************************

Here is the sample code::

    from pyexcel import Reader
    from pyexcel.ext import ods3
    from pyexcel.utils import to_array
    import json
    
    # "example.ods"
    reader = Reader("example.ods")
    data = to_array(reader)
    print json.dumps(data)

Writing to an ods file
**********************

Here is the sample code::

    from pyexcel import Writer
    from pyexcel.ext import ods3
    
    array = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    writer = Writer("output.ods")
    writer.write_array(array)
    writer.close()

Reading from a StringIO instance
================================

You got to wrap the binary content with StringIO to get odf working::


    import pyexcel
    from pyexcel.ext import ods3
    from StringIO import StringIO # for py3, from io import BytesIO as StringIO

    # This is just an illustration
    # In reality, you might deal with ods file upload
    # where you will read from requests.FILES['YOUR_ODS_FILE']
    odsfile = "example.ods"
    with open(odsfile, "rb") as f:
        content = f.read()
        r = pyexcel.Reader(("ods", StringIO(content)))


Writing to a StringIO instance
================================

You need to pass a StringIO instance to Writer::

    import pyexcel
    from pyexcel.ext import ods3
    from StringIO import StringIO # for py3, from io import BytesIO as StringIO


    data = [
        [1, 2, 3],
        [4, 5, 6]
    ]
    io = StringIO()
    w = pyexcel.Writer(("ods",io))
    w.write_rows(data)
    w.close()
    # then do something with io
    # In reality, you might give it to your http response
    # object for downloading


Dependencies
============

1. ezodf


Test coverage
==============

`code coverage <https://codecov.io/github/chfw/pyexcel-ods3>`_
