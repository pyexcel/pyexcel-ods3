# pyexcel-ods3 [![Build Status](https://api.travis-ci.org/chfw/pyexcel-ods3.png)](http://travis-ci.org/chfw/pyexcel-ods3)

**pyexcel-ods** is a plugin to pyexcel and provides the capbility to read, manipulate and write data in ods fromats using python 2.6 and python 2.7

# usage

```python
import pyexcel_ods3
from pyexcel import Reader
from pyexcel.utils import to_array
import json

# "example.xls","example.xlsx","example.ods", "example.xlsm"
reader = Reader("example.csv")
data = to_array(reader)
print json.dumps(data)
```

## Dependencies

* lxml
* ezodf2
