#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request
from gevent.pywsgi import WSGIServer
import inspect
import json
import sys

app = Flask(__name__)

#DEBUG=True
DEBUG=False

app.debug = DEBUG

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

@app.route("/inventory")
def index():
    if DEBUG:
        print(inspect.currentframe().f_code.co_name)
    return render_template("/inventory/index.html")

if __name__ == '__main__':
    if DEBUG:
        app.run(host='0.0.0.0', port=8080)
    else:
        http_server = WSGIServer(('0.0.0.0', 8080), app)
        http_server.serve_forever()
