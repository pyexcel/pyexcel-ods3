try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

with open("README.rst", 'r') as readme:
    README_txt = readme.read()

with open("requirements.txt", 'r') as dependencies:
    lines = dependencies.readlines()
    lines = map(lambda x: x.rstrip(), lines)
    requirements_txt = lines

with open("VERSION", "r") as version:
    version_txt = version.read().rstrip()

setup(
    name='pyexcel-ods3',
    author="C. W.",
    version=version_txt,
    author_email="wangc_2011@hotmail.com",
    url="https://github.com/chfw/pyexcel-ods3",
    description='A wrapper library to read, manipulate and write data in ods format',
    install_requires=requirements_txt,
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    long_description=README_txt,
    zip_safe=False,
    tests_require=['nose'],
    license='New BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Office/Business',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ]
)
