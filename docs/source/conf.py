# -*- coding: utf-8 -*-
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]

intersphinx_mapping = {
    'pyexcel': ('http://pyexcel.readthedocs.org/en/latest/', None)
}
spelling_word_list_filename = 'spelling_wordlist.txt'
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = u'pyexcel-ods3'
copyright = u'2015-2016 Onni Software Ltd.'
version = '0.2.0'
release = '0.2.1'
exclude_patterns = []
pygments_style = 'sphinx'
html_theme = 'default'
html_static_path = ['_static']
htmlhelp_basename = 'pyexcel-ods3doc'
latex_elements = {}
latex_documents = [
    ('index', 'pyexcel-ods3.tex', u'pyexcel-ods3 Documentation',
     'Onni Software Ltd.', 'manual'),
]
man_pages = [
    ('index', 'pyexcel-ods3', u'pyexcel-ods3 Documentation',
     [u'Onni Software Ltd.'], 1)
]
texinfo_documents = [
    ('index', 'pyexcel-ods3', u'pyexcel-ods3 Documentation',
     'Onni Software Ltd.', 'pyexcel-ods3', 'One line description of project.',
     'Miscellaneous'),
]
