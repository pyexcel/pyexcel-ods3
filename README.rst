================================================================================
pyexcel-ods3 - Let you focus on data, instead of ods format
================================================================================

.. image:: https://raw.githubusercontent.com/pyexcel/pyexcel.github.io/master/images/patreon.png
   :target: https://www.patreon.com/pyexcel

.. image:: https://api.travis-ci.org/pyexcel/pyexcel-ods3.svg?branch=master
   :target: http://travis-ci.org/pyexcel/pyexcel-ods3

.. image:: https://codecov.io/github/pyexcel/pyexcel-ods3/coverage.png
   :target: https://codecov.io/github/pyexcel/pyexcel-ods3


**pyexcel-ods3** is a tiny wrapper library to read, manipulate and write data in ods
format. You are likely to use `pyexcel <https://github.com/pyexcel/pyexcel>`__ together
with this library. `pyexcel-ods <https://github.com/pyexcel/pyexcel-ods>`__ is a sister
library that depends on GPL licensed odfpy.
`pyexcel-odsr <https://github.com/pyexcel/pyexcel-odsr>`_ is the other sister library
that has no external dependency but do ods reading only

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

    $ git clone https://github.com/pyexcel/pyexcel-ods3.git
    $ cd pyexcel-ods3
    $ python setup.py install

Support the project
================================================================================

If your company has embedded pyexcel and its components into a revenue generating
product, please `support me on patreon <https://www.patreon.com/bePatron?u=5537627>`_ to
maintain the project and develop it further.

If you are an individual, you are welcome to support me too on patreon and for however long
you feel like to. As a patreon, you will receive
`early access to pyexcel related contents <https://www.patreon.com/pyexcel/posts>`_.

With your financial support, I will be able to invest
a little bit more time in coding, documentation and writing interesting posts.


Usage
================================================================================

As a standalone library
--------------------------------------------------------------------------------

.. testcode::
   :hide:

    >>> import os
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


Write to an ods file
********************************************************************************



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


Pagination feature
********************************************************************************

Special notice 30/01/2017: due to the constraints of the underlying 3rd party
library, it will read the whole file before returning the paginated data. So
at the end of day, the only benefit is less data returned from the reading
function. No major performance improvement will be seen.

With that said, please install `pyexcel-odsr <https://github.com/pyexcel/pyexcel-odsr>`_
and it gives better performance in pagination.

Let's assume the following file is a huge ods file:

.. code-block:: python

   >>> huge_data = [
   ...     [1, 21, 31],
   ...     [2, 22, 32],
   ...     [3, 23, 33],
   ...     [4, 24, 34],
   ...     [5, 25, 35],
   ...     [6, 26, 36]
   ... ]
   >>> sheetx = {
   ...     "huge": huge_data
   ... }
   >>> save_data("huge_file.ods", sheetx)

And let's pretend to read partial data:

.. code-block:: python

   >>> partial_data = get_data("huge_file.ods", start_row=2, row_limit=3)
   >>> print(json.dumps(partial_data))
   {"huge": [[3, 23, 33], [4, 24, 34], [5, 25, 35]]}

And you could as well do the same for columns:

.. code-block:: python

   >>> partial_data = get_data("huge_file.ods", start_column=1, column_limit=2)
   >>> print(json.dumps(partial_data))
   {"huge": [[21, 31], [22, 32], [23, 33], [24, 34], [25, 35], [26, 36]]}

Obvious, you could do both at the same time:

.. code-block:: python

   >>> partial_data = get_data("huge_file.ods",
   ...     start_row=2, row_limit=3,
   ...     start_column=1, column_limit=2)
   >>> print(json.dumps(partial_data))
   {"huge": [[23, 33], [24, 34], [25, 35]]}

.. testcode::
   :hide:

   >>> os.unlink("huge_file.ods")


As a pyexcel plugin
--------------------------------------------------------------------------------

No longer, explicit import is needed since pyexcel version 0.2.2. Instead,
this library is auto-loaded. So if you want to read data in ods format,
installing it is enough.


Reading from an ods file
********************************************************************************

Here is the sample code:

.. code-block:: python

    >>> import pyexcel as pe
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
********************************************************************************

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
********************************************************************************

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

Upgrade your setup tools and pip. They are needed for development and testing only:

#. pip install --upgrade setuptools pip

Then install relevant development requirements:

#. pip install -r rnd_requirements.txt # if such a file exists
#. pip install -r requirements.txt
#. pip install -r tests/requirements.txt


In order to update test environment, and documentation, additional steps are
required:

#. pip install moban
#. git clone https://github.com/pyexcel/pyexcel-commons.git commons
#. make your changes in `.moban.d` directory, then issue command `moban`

What is rnd_requirements.txt
-------------------------------

Usually, it is created when a dependent library is not released. Once the dependecy is installed(will be released), the future version of the dependency in the requirements.txt will be valid.

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

    $ make

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
