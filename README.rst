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


**pyexcel-ods3** is a tiny wrapper library to read, manipulate and write data in ods fromat using python 2.7, python 3.3 and python 3.4. You are likely to use pyexcel instead of this plugin. `pyexcel-ods <https://github.com/chfw/pyexcel-ods>`_ is a sister library that does the same thing but supports python 2.6 and has no dependency on lxml.


Installation
============

You can install it via pip::

    $ pip install pyexcel-ods3


or clone it and install it::

    $ git clone http://github.com/chfw/pyexcel-ods3.git
    $ cd pyexcel
    $ python setup.py install


The installation of `lxml` will be tricky on Widnows platform. It recommended that you download a lxml's own windows installer instead of using pip.


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

As a pyexcel plugin
--------------------

Import it in your file to enable this plugin::

    from pyexcel.ext import ods3

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


Dependencies
============

1. lxml
2. ezodf2


Test coverage
==============

`code coverage <https://codecov.io/github/chfw/pyexcel-ods3>`_
