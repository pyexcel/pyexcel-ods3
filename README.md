# pyexcel-ods [![Build Status](https://api.travis-ci.org/chfw/pyexcel-ods.png)](http://travis-ci.org/chfw/pyexcel-ods)

**pyexcel-ods** is a plugin to pyexcel and provides the capbility to read, manipulate and write data in ods fromats using python 2.6 and python 2.7

# usage

```python
import pyexcel_ods
from pyexcel import Reader
from pyexcel.utils import to_array
import json

# "example.xls","example.xlsx","example.ods", "example.xlsm"
reader = Reader("example.csv")
data = to_array(reader)
print json.dumps(data)
```

## Dependencies

* odfpy

## Credits

ODSReader is written by [Marco Conti](https://github.com/marcoconti83/read-ods-with-odfpy)