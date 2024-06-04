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
    ig = [] # groups should be included
    eg = [] # groups should be excluded
    eu = [] # users should be excluded
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
    info = request.get_json(force=True)
    ig = [] # groups should be included
    eg = [] # groups should be excluded
    eu = [] # users should be excluded
    iu = [] # users should be included
    arguments = {'expires' : 0, 'create_home' : 'no'}
    try:
        if 'ig' in info:
            ig = info['ig']
        if 'eg' in info:
            eg = info['eg']
        if 'eu' in info:
            eu = info['eu']
        if 'iu' in info:
            iu = info['iu']
        if 'args' in info:
            if len(info['args']) == 2:
                if 'expires' in info['args'] and 'create_home' in info['args']:
                    arguments = info['args']
    except:
        text = "Incorrect json data filling!"
        return jsonify(result=text)

    groups = getGroups(excluded = eg, included = ig, excludedUsers = eu);
    users = getUsers(excluded = eu, included = iu);
    playbook = getUsersPlayBook(users, groups, arguments, included = iu)
    writePlayBook(playbook, "users_playbook.yml")
    return send_from_directory(app.root_path, "users_playbook.yml")

if __name__ == '__main__':
    if DEBUG:
        app.run(host='0.0.0.0', port=8080)
    else:
        http_server = WSGIServer(('0.0.0.0', 8080), app)
        http_server.serve_forever()
