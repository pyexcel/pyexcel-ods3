{% extends 'setup.py.jj2' %}

{%block extras %}
import sys
if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    dependencies.append('weakrefset')
{%endblock%}

{%block additional_keywords%}
    'ods'
{%endblock%}

{%block additional_classifiers%}
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5'
{%endblock%}}
