# Inventory of access
[![Python application](https://github.com/mperov/inventory-of-access/workflows/Python%20application/badge.svg?branch=master)](https://github.com/mperov/inventory-of-access/actions/workflows/python-app.yml)
[![Contributors](https://img.shields.io/github/contributors/mperov/showGroups?label=Contributors)](https://github.com/mperov/showGroups/graphs/contributors)

## Description

In OS Linux there are files - **/etc/passwd** and **/etc/groups**, which aren't informateble if you watch these via text editors.  
So **inventory-of-access** tris to help you to get informations about users in Linux and about participants of groups.

Moreover this project can help to synchronize users and groups in clusters. In most cases clusters are based on NFS servers.
NFS server requires synchronized UIDs and GIDs on all machines in clusters.

## How to start
1. Get project:
```console
$ git clone --recursive https://github.com/mperov/inventory-of-access.git
$ cd inventory-of-access/
```
2. Create special Python virtual enviroment by
```console
$ sudo apt-get install python3-venv -y
$ python3 -m venv inventory-of-access
$ source inventory-of-access/bin/activate
```
3. Install some Python modules - `pip3 install -r requirements` or `python3 -m pip install -r requirements`  
If you don't have pip3 then you may install it [how described here](https://pip.pypa.io/en/stable/installation/)

## How to use

There are three main ways using of inventory-of-access.

#### The frist - showing some tables
It allows to understand what users are in what groups:  
```
$ ./inventory.py -m table
+-------+-----+-------+------+-----+-------+
| users | adm | cdrom | sudo | tty | voice |
+-------+-----+-------+------+-----+-------+
| coder |  +  |   +   |  +   |  -  |   +   |
+-------+-----+-------+------+-----+-------+
```

It shows UID and GID for all users:
```
$ ./inventory.py -m user
+-------+------+------+
| users | UID  | GID  |
+-------+------+------+
| coder | 1000 | 1000 |
+-------+------+------+
```

This mode helps to get GID for each groups:
```
$ ./inventory.py -m group
+--------------+-----+
|    groups    | GID |
+--------------+-----+
|     adm      |  4  |
|     tty      |  5  |
|    voice     |  22 |
|    cdrom     |  24 |
|     sudo     |  27 |
+--------------+-----+
```

#### The second - generating Ansible playbook

This generates the playbook is used for adding groups. It can help to add groups on all machine on a cluster via ansible.
```
$ ./inventory.py yaml -t groups
YAML is successfully generating to playbook.yml
This file should be in your current directory!
```
So let's see generated playbook.
```
$ cat playbook.yml
---
- name: Add additional groups
  hosts: all
  become: yes
  tasks:
  - name: adding adm
    group:
      name: adm
      gid: '4'
  - name: adding tty
    group:
      name: tty
      gid: '5'
  - name: adding voice
    group:
      name: voice
      gid: '22'
  - name: adding cdrom
    group:
      name: cdrom
      gid: '24'
  - name: adding sudo
    group:
      name: sudo
      gid: '27'
```

It generates ansible playbook for adding users.
```
$ ./inventory.py yaml -t users
YAML is successfully generating to playbook.yml
This file should be in your current directory!
```
As you can see we got playbook:
```
$ cat playbook.yml
---
- name: Add user with UID, GID and additional groups
  hosts: all
  become: yes
  tasks:
  - name: adding coder
    user:
      name: coder
      append: yes
      uid: '1000'
      group: '1000'
      expires: 0
      create_home: no
      groups: adm,voice,cdrom,sudo
```

Let's see some parameters:  
1) `expires: 0` is needed to block ssh access to nodes from master machine. Users should only use cluster scheduler, e.g. slurm, AGE, SGE, et cetera.  
2) `create_home: no` turns off creating home directory for adding user. Home directory was created when user was added to master machine.

#### The third - web server to generate Ansible playbook

1. **On server**: start WEB server on 8080 port:  
```console
$ ./webApp.py
```
2. **On client**: get generated ansible playbook via http for adding groups:  
```console
$ curl -H "Content-Type: application/json" -X POST --data '{"ig" : [] , "eg" : ["lxd", "video", "plugdev", "adm"], "eu" : []}' -sS http://localhost:8080/inventory/groups
---
- name: Add additional groups
  hosts: '{{ HOST }}'
  become: yes
  tasks:
  - name: adding tty
    group:
      name: tty
      gid: '5'
  - name: adding voice
    group:
      name: voice
      gid: '22'
  - name: adding cdrom
    group:
      name: cdrom
      gid: '24'
  - name: adding sudo
    group:
      name: sudo
      gid: '27'
```  
"ig" is "included groups"  
"eg" means "excluded groups"  
"eu" means "excluded users"  
3. **On client**: get generated ansible playbook via http for adding users with right permissions:  
```console
$ curl -H "Content-Type: application/json" -X POST --data '{"eg" : ["lxd", "video", "plugdev", "adm", "cdrom"], "iu" : "root,coder"}' -sS http://localhost:8080/inventory/users
---
- name: Add user with UID, GID and additional groups
  hosts: '{{ HOST }}'
  become: yes
  tasks:
  - name: adding root
    user:
      name: root
      append: yes
      uid: '0'
      group: '0'
      home: /root
      expires: 0
      create_home: no
      groups: ''
  - name: adding coder
    user:
      name: coder
      append: yes
      uid: '1000'
      group: '1000'
      home: /home/coder
      expires: 0
      create_home: no
      groups: voice,sudo,audio,dip,lpadmin,pulse,pulse-access,sambashare
```  
"eg" means "excluded groups"  
"iu" means "included users"
