# -*- coding: utf-8 -*-

#
# Copyright (c) 2022 Maksim Perov <coder@frtk.ru>
#

import sys
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO

FILE_PLAYBOOK = "playbook.yml"

class CustomYAML(YAML):
    def dump(self, data, stream=None, **kw):
        inefficient = False
        if stream is None:
            inefficient = True
            stream = StringIO()
        YAML.dump(self, data, stream, **kw)
        if inefficient:
            return stream.getvalue()

def getPingPlayBook():
    content = [ # using list allows to prepend '-' (dash symbol)
                {
                    'name'  : 'Ping pong',
                    'hosts' : 'all',
                    'tasks' :
                    [ # using list allows to prepend '-' (dash symbol)
                        {
                            'name' : 'Ping',
                            'ping' : None,
                        }
                    ],
                }
              ]
    yaml = CustomYAML()
    yaml.explicit_start = True # --- at the beginning of yaml
    return yaml.dump(content)

def getUsersPlayBook(users = [], groups = [], args = {'expires' : 0, 'create_home' : 'no'}):
    content = [
                {
                    'name'      : 'Add user with UID, GID and additional groups',
                    'hosts'     : 'all',
                    'become'    : 'yes',
                }
              ]
    tasks = []
    for user in users:
        task = {
                'name' : 'adding ' + user,
                'user' : {
                            'name'          : user,
                            'append'        : 'yes',
                            'uid'           : str(users[user][0]),
                            'group'         : str(users[user][1]),
                         }
               }
        task['user'].update(args)
        grp = []
        for group in groups:
            if user in groups[group]['users']:
                grp.append(group)
        grps = ','.join(grp)
        task['user'].update({'groups' : grps})
        if grps != '':
            tasks.append(task)
    content[0].update({ 'tasks' : tasks })
    yaml = CustomYAML()
    yaml.explicit_start = True # --- at the beginning of yaml
    return yaml.dump(content)

def getGroupsPlayBook(groups = []):
    content = [
                {
                    'name'      : 'Add additional groups',
                    'hosts'     : 'all',
                    'become'    : 'yes',
                }
              ]
    tasks = []
    for group in groups:
        task = {
                'name' : 'adding ' + group,
                'group' : {
                            'name'  : group,
                            'gid'   : groups[group]['GID']
                          }
               }
        tasks.append(task)
    content[0].update({ 'tasks' : tasks })
    yaml = CustomYAML()
    yaml.explicit_start = True # --- at the beginning of yaml
    return yaml.dump(content)

def writePlayBook(playbook = getPingPlayBook()):
    try:
        with open(FILE_PLAYBOOK , "w") as f:
            f.write(playbook)
    except Exception as e:
        print("ERROR: " + FILE_PLAYBOOK + " isn't writable!")
        print(str(e))
        sys.exit(-1)
    print('YAML is successfully generating to ' + FILE_PLAYBOOK)
    print('This file should be in your current directory!')
