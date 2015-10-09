#!/usr/bin/env python
from wsgiref import simple_server
from urls import *

if __name__ == '__main__':
    httpd = simple_server.make_server('0.0.0.0', 8003, app)
    httpd.serve_forever()
