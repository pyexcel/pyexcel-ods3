try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

with open("README.rst", 'r') as readme:
    README_txt = readme.read()

with open("CHANGELOG.rst", 'r') as changelog:
    README_txt += changelog.read()

dependencies = [
    'pyexcel-io>=0.1.0',
    'lxml',
    'ezodf>=0.3.2',
]

extras = {}

import sys
if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    dependencies.append('weakrefset')

setup(
    name='pyexcel-ods3',
    author='C.W.',
    version='0.2.0',
    author_email='wangc_2011 (at) hotmail.com',
    url='https://github.com/pyexcel/pyexcel-ods3',
    description='A wrapper library to read, manipulate and write data in ods format',
    install_requires=dependencies,
    extras_require=extras,
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    long_description=README_txt,
    zip_safe=False,
    tests_require=['nose'],
    keywords=[
        'excel',
        'python',
        'pyexcel',
        'ods'
    ],
    license='New BSD',
    classifiers=[
        'Topic :: Office/Business',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ]
)