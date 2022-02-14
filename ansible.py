# -*- coding: utf-8 -*-

#
# Copyright (c) 2022 Maksim Perov <coder@frtk.ru>
#

from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO

class CustomYAML(YAML):
    def dump(self, data, stream=None, **kw):
        inefficient = False
        if stream is None:
            inefficient = True
            stream = StringIO()
        YAML.dump(self, data, stream, **kw)
        if inefficient:
            return stream.getvalue()

def getPlayBook():
    content = [
                {
                    'name'  : 'Ping pong',
                    'hosts' : 'all',
                    'tasks' :
                    [
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
