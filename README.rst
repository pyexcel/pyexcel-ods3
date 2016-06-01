================================================================================
pyexcel-ods3 - Let you focus on data, instead of ods format
================================================================================

.. image:: https://api.travis-ci.org/pyexcel/pyexcel-ods3.png
    :target: http://travis-ci.org/pyexcel/pyexcel-ods3

.. image:: https://codecov.io/github/pyexcel/pyexcel-ods3/coverage.png
    :target: https://codecov.io/github/pyexcel/pyexcel-ods3

**pyexcel-ods3** is a tiny wrapper library to read, manipulate and write data in ods format using python version 2.6(since v0.0.8), 2.7, 3.3 and 3.4. You are likely to use `pyexcel <https://github.com/pyexcel/pyexcel>`__ together with this library. `pyexcel-ods <https://github.com/pyexcel/pyexcel-ods>`__ is a sister library, having no dependency on lxml. However it has no support for python 3.

Known constraints
==================

Fonts, colors and charts are not supported.

Installation
================================================================================

You can install it via pip:

.. code-block:: bash

    $ pip install pyexcel-ods3


or clone it and install it:

.. code-block:: bash

    $ git clone http://github.com/pyexcel/pyexcel-ods3.git
    $ cd pyexcel-ods3
    $ python setup.py install

Usage
================================================================================

As a standalone library
--------------------------------------------------------------------------------

Write to an ods file
********************************************************************************

.. testcode::
   :hide:

    >>> import sys
    >>> if sys.version_info[0] < 3:
    ...     from StringIO import StringIO
    ... else:
    ...     from io import BytesIO as StringIO
    >>> PY2 = sys.version_info[0] == 2
    >>> if PY2 and sys.version_info[1] < 7:
    ...      from ordereddict import OrderedDict
    ... else:
    ...     from collections import OrderedDict


Here's the sample code to write a dictionary to an ods file:

.. code-block:: python

    >>> from pyexcel_ods3 import save_data
    >>> data = OrderedDict() # from collections import OrderedDict
    >>> data.update({"Sheet 1": [[1, 2, 3], [4, 5, 6]]})
    >>> data.update({"Sheet 2": [["row 1", "row 2", "row 3"]]})
    >>> save_data("your_file.ods", data)

Read from an ods file
********************************************************************************

Here's the sample code:

.. code-block:: python

    >>> from pyexcel_ods3 import get_data
    >>> data = get_data("your_file.ods")
    >>> import json
    >>> print(json.dumps(data))
    {"Sheet 1": [[1, 2, 3], [4, 5, 6]], "Sheet 2": [["row 1", "row 2", "row 3"]]}

Write an ods to memory
********************************************************************************

Here's the sample code to write a dictionary to an ods file:

.. code-block:: python

    >>> from pyexcel_ods3 import save_data
    >>> data = OrderedDict()
    >>> data.update({"Sheet 1": [[1, 2, 3], [4, 5, 6]]})
    >>> data.update({"Sheet 2": [[7, 8, 9], [10, 11, 12]]})
    >>> io = StringIO()
    >>> save_data(io, data)
    >>> # do something with the io
    >>> # In reality, you might give it to your http response
    >>> # object for downloading


.. testcode::
   :hide: 

    >>> notneeded=io.seek(0)

Read from an ods from memory
********************************************************************************

Continue from previous example:

.. code-block:: python

    >>> # This is just an illustration
    >>> # In reality, you might deal with ods file upload
    >>> # where you will read from requests.FILES['YOUR_ODS_FILE']
    >>> data = get_data(io)
    >>> print(json.dumps(data))
    {"Sheet 1": [[1, 2, 3], [4, 5, 6]], "Sheet 2": [[7, 8, 9], [10, 11, 12]]}


As a pyexcel plugin
--------------------------------------------------------------------------------

No longer, explicit import is needed since pyexcel version 0.2.2. Instead,
this library is auto-loaded. So if you want to read data in ods format,
installing it is enough.

Any version under pyexcel 0.2.2, you have to keep doing the following:

Import it in your file to enable this plugin:

.. code-block:: python

    from pyexcel.ext import ods3

Please note only pyexcel version 0.0.4+ support this.

Reading from an ods file
********************************************************************************

Here is the sample code:

.. code-block:: python

    >>> import pyexcel as pe
    >>> # from pyexcel.ext import ods3
    >>> sheet = pe.get_book(file_name="your_file.ods")
    >>> sheet
    Sheet 1:
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    Sheet 2:
    +-------+-------+-------+
    | row 1 | row 2 | row 3 |
    +-------+-------+-------+

Writing to an ods file
********************************************************************************

Here is the sample code:

.. code-block:: python

    >>> sheet.save_as("another_file.ods")

Reading from a IO instance
================================================================================

You got to wrap the binary content with stream to get ods working:

.. code-block:: python

    >>> # This is just an illustration
    >>> # In reality, you might deal with ods file upload
    >>> # where you will read from requests.FILES['YOUR_ODS_FILE']
    >>> odsfile = "another_file.ods"
    >>> with open(odsfile, "rb") as f:
    ...     content = f.read()
    ...     r = pe.get_book(file_type="ods", file_content=content)
    ...     print(r)
    ...
    Sheet 1:
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    Sheet 2:
    +-------+-------+-------+
    | row 1 | row 2 | row 3 |
    +-------+-------+-------+


Writing to a StringIO instance
================================================================================

You need to pass a StringIO instance to Writer:

.. code-block:: python

    >>> data = [
    ...     [1, 2, 3],
    ...     [4, 5, 6]
    ... ]
    >>> io = StringIO()
    >>> sheet = pe.Sheet(data)
    >>> io = sheet.save_to_memory("ods", io)
    >>> # then do something with io
    >>> # In reality, you might give it to your http response
    >>> # object for downloading

License
================================================================================

New BSD License

Developer guide
==================

Development steps for code changes

#. git clone https://github.com/pyexcel/pyexcel-ods3.git
#. cd pyexcel-ods3
#. pip install -r rnd_requirements.txt # if such a file exists
#. pip install -r requirements.txt
#. pip install -r tests/requirements.txt


In order to update test envrionment, and documentation, additional setps are
required:

#. pip install moban
#. git clone https://github.com/pyexcel/pyexcel-commons.git
#. make your changes in `.moban.d` directory, then issue command `moban`

What is rnd_requirements.txt
-------------------------------

Usually, it is created when a depdent library is not released. Once the dependecy is installed(will be released), the future version of the dependency in the requirements.txt will be valid.

What is pyexcel-commons
---------------------------------

Many information that are shared across pyexcel projects, such as: this developer guide, license info, etc. are stored in `pyexcel-commons` project.

What is .moban.d
---------------------------------

`.moban.d` stores the specific meta data for the library.

How to test your contribution
------------------------------

Although `nose` and `doctest` are both used in code testing, it is adviable that unit tests are put in tests. `doctest` is incorporated only to make sure the code examples in documentation remain valid across different development releases.

On Linux/Unix systems, please launch your tests like this::

    $ make test

On Windows systems, please issue this command::

    > test.bat

Installation Note
================================================================================
The installation of `lxml` will be tricky on Windows platform. It is recommended that you download a lxml's own windows installer instead of using pip.

.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("your_file.ods")
   >>> os.unlink("another_file.ods")
