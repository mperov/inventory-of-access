#!/bin/bash

curl -H "Content-Type: application/json" -X POST --data '{"ig" : [] , "eg" : ["lxd", "video", "plugdev", "adm"]}' -sS http://localhost:8080/inventory/groups -o groups_playbook.yml
ansible-playbook --syntax-check groups_playbook.yml -e HOST=localhost

curl -H "Content-Type: application/json" -X POST --data '{"eg" : ["lxd", "video", "plugdev", "adm", "cdrom"], "iu" : "root,coder"}' -sS http://localhost:8080/inventory/users -o users_playbook.yml
ansible-playbook --syntax-check users_playbook.yml -e HOST=localhost
