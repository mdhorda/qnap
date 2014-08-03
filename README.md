qnap
====

QNAP is a network attached storage device that comes with Linux installed on it. They provide a REST API for doing operations on files stored on the device. This repository contains a Python binding for the QNAP NAS API. The following operations are currently supported:

- List shares
- List directory
- Get file info
- Search files
- Delete files
- Download files
- Upload files

The API has been tested with Python 2.7.5 and a QNAP TS-269L. Sample usage:

```python
host = 'usademo.myqnapcloud.com'
user = 'qnap'
password = 'qnap'

filestation = FileStation(host, user, password)
shares = filestation.list_share()
file_list = filestation.list('/Multimedia')
search_results = filestation.search('/Multimedia/Sample/picture', 'sample')
file_contents = filestation.download('/Multimedia/Sample/picture/sample001.jpg')
```
