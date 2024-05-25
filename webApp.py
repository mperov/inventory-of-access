#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request, send_from_directory
from gevent.pywsgi import WSGIServer
import inspect
import json
import sys
from inventory import getGroups, getUsers
from ansible import getGroupsPlayBook, getUsersPlayBook, writePlayBook

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

@app.route('/inventory/groups', methods=["GET", "POST"])
def sendGroups():
    if DEBUG:
        print(inspect.currentframe().f_code.co_name)
    info = request.get_json(force=True)
    ig = []
    eg = []
    eu = []
    try:
        if 'ig' in info:
            ig = info['ig']
        if 'eg' in info:
            eg = info['eg']
        if 'eu' in info:
            eu = info['eu']
    except:
        text = "Incorrect json data filling!"
        return jsonify(result=text)

    groups = getGroups(excluded = eg, included = ig, excludedUsers = eu);
    playbook = getGroupsPlayBook(groups)
    writePlayBook(playbook, "groups_playbook.yml")
    return send_from_directory(app.root_path, "groups_playbook.yml")

@app.route('/inventory/users', methods=["GET", "POST"])
def sendUsers():
    if DEBUG:
        print(inspect.currentframe().f_code.co_name)
    groups = getGroups();
    users = getUsers();
    playbook = getUsersPlayBook(users, groups)
    writePlayBook(playbook, "users_playbook.yml")
    return send_from_directory(app.root_path, "users_playbook.yml")

if __name__ == '__main__':
    if DEBUG:
        app.run(host='0.0.0.0', port=8080)
    else:
        http_server = WSGIServer(('0.0.0.0', 8080), app)
        http_server.serve_forever()
