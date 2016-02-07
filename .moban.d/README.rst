{%extends 'README.rst.jj2' %}

{%block description%}
**pyexcel-ods3** is a tiny wrapper library to read, manipulate and write data in ods fromat using python version 2.6(since v0.0.8), 2.7, 3.3 and 3.4. You are likely to use `pyexcel <https://github.com/pyexcel/pyexcel>`__ together with this library. `pyexcel-ods <https://github.com/pyexcel/pyexcel-ods>`__ is a sister library, having no dependency on lxml. However it has no support for python 3.
{%endblock%}

{%block middle_block%}
.. testcode::
   :hide: 

    >>> notneeded=io.seek(0)
{%endblock%}

{%block extras %}
Installation Note
================================================================================
The installation of `lxml` will be tricky on Windows platform. It is recommended that you download a lxml's own windows installer instead of using pip.
{%endblock%}
