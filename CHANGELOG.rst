Change log
================================================================================

0.2.2 - 05.11.2016
--------------------------------------------------------------------------------

Updated
********************************************************************************

#. `#11 <https://github.com/pyexcel/pyexcel-ods3/issues/11>`_, be able to
   consume a generator of two dimensional arrays.


0.2.1 - 31.08.2016
--------------------------------------------------------------------------------

Added
********************************************************************************

#. support pagination. two pairs: start_row, row_limit and start_column,
   column_limit help you deal with large files.


0.2.0 - 01.06.2016
--------------------------------------------------------------------------------

Added
********************************************************************************

#. By default, `float` will be converted to `int` where fits. `auto_detect_int`,
   a flag to switch off the autoatic conversion from `float` to `int`.
#. 'library=pyexcel-ods3' was added so as to inform pyexcel to use it instead
   of other libraries, in the situation where multiple plugins for the same
   file type are installed


Updated
********************************************************************************

#. support the auto-import feature of pyexcel-io 0.2.0


0.1.0 - 17.01.2016
--------------------------------------------------------------------------------

#. compatibility with pyexcel-io 0.1.0
