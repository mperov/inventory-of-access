#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from prettytable import PrettyTable

def getUsers():
    users = {}
    with open("/etc/passwd" , "r") as f:
        for line in f.readlines():
            splited = line.split(":")
            shell = splited[-1:][0].split('\n')[0].split('/')[-1:][0]
            homePath = splited[-2:][0].split('/')
            if 'home' in homePath and shell in ['bash', 'sh']:
                users.update({splited[0] : [splited[2], splited[3]]})
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

def showPretty(users, groups):
    table = PrettyTable(['users'] + list(groups))
    for user in users:
        marks = []
        for group in groups:
            if user in groups[group]:
                marks.append('+')
            else:
                marks.append('-')
        table.add_row([user] + marks)
    print(table)

if __name__ == "__main__":
    print(getGroups())
