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

def getGroups():
    groups = []
    with open("/etc/group" , "r") as f:
        for line in f.readlines():
            groups.append(line.split(":")[0])
    return groups

if __name__ == "__main__":
    print(getGroups())
