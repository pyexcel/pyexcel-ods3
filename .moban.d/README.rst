{%extends 'README.rst.jj2' %}

{%block description%}
**pyexcel-ods3** is a tiny wrapper library to read, manipulate and write data in ods
format. You are likely to use `pyexcel <https://github.com/pyexcel/pyexcel>`__ together
with this library. `pyexcel-ods <https://github.com/pyexcel/pyexcel-ods>`__ is a sister
library that depends on GPL licensed odfpy.
`pyexcel-odsr <https://github.com/pyexcel/pyexcel-odsr>`_ is the other sister library
that has no external dependency but do ods reading only
{%endblock%}

{%block middle_block%}
.. testcode::
   :hide: 

    >>> notneeded=io.seek(0)
{%endblock%}

{% block pagination_note%}
Special notice 30/01/2017: due to the constraints of the underlying 3rd party
library, it will read the whole file before returning the paginated data. So
at the end of day, the only benefit is less data returned from the reading
function. No major performance improvement will be seen.

With that said, please install `pyexcel-odsr <https://github.com/pyexcel/pyexcel-odsr>`_
and it gives better performance in pagination.
{%endblock%}

{%block extras %}
Installation Note
================================================================================
The installation of `lxml` will be tricky on Windows platform. It is recommended that you download a lxml's own windows installer instead of using pip.
{%endblock%}
