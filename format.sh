isort $(find pyexcel_ods3 -name "*.py"|xargs echo) $(find tests -name "*.py"|xargs echo)
black -l 79 pyexcel_ods3
black -l 79 tests
