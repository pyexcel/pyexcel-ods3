pip freeze
nosetests --with-cov --cover-package pyexcel_ods3 --cover-package tests --with-doctest --doctest-extension=.rst README.rst tests docs/source pyexcel_ods3 && flake8 . --exclude=.moban.d --builtins=unicode,xrange,long
