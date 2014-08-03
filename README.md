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

The API has been tested with Python 2.7.5 and a QNAP TS-269L.
