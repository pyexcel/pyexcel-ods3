"""
    pyexcel-ods3
    ~~~~~~~~~~~~~~

    It is a plugin to pyexcel and provides the capbility to read, manipulate and write data in ods fromats using python 3.4, 3.2 and python 2.7. 
"""

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='pyexcel-ods3',
    author="C. W.",
    version='0.0.1',
    author_email="wangc_2011@hotmail.com",
    url="https://github.com/chfw/pyexcel-odf",
    description='A wrapper library to read, manipulate and write data in odf format',
    install_requires=[
        'lxml',
        "ezodf2"
    ],
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    long_description=__doc__,
    zip_safe=False,
    tests_require=['nose'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Office/Business',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU General Public License v3',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.4'
        
    ]
)
