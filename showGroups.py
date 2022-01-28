#!/usr/bin/env python3
# -*- coding: utf-8 -*-

TARGET_GROUPS = [ ]

def getUsers():
    users = []
    with open("/etc/passwd" , "r") as f:
        for line in f.readlines():
            splited = line.split(":")
            shell = splited[-1:][0].split('\n')[0].split('/')[-1:][0]
            homePath = splited[-2:][0].split('/')
            if 'home' in homePath and shell in ['bash', 'sh']:
                users.append(splited[0])
    return users

def getGroups(excluded = []):
    groups = {}
    with open("/etc/group" , "r") as f:
        for line in f.readlines():
            _list = line.split(":")
            name = _list[0]
            participants = _list[3]
            if participants.strip() != '' and name not in excluded:
                groups.update({ name : participants.split('\n')[0].split(',') })
    return groups

if __name__ == "__main__":
    print(getGroups())
