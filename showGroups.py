#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from prettytable import PrettyTable

def getUsers(excluded = []):
    users = {}
    with open("/etc/passwd" , "r") as f:
        for line in f.readlines():
            splited = line.split(":")
            shell = splited[-1:][0].split('\n')[0].split('/')[-1:][0]
            homePath = splited[-2:][0].split('/')
            name = splited[0]
            if 'home' in homePath and shell in ['bash', 'sh'] and name not in excluded:
                users.update({name : [splited[2], splited[3]]})
    return users

def getGroups(excluded = []):
    groups = {}
    with open("/etc/group" , "r") as f:
        for line in f.readlines():
            _list = line.split(":")
            name = _list[0]
            participants = _list[3]
            if participants.strip() != '' and name not in excluded:
                groups.update({ (name, _list[2]) : participants.split('\n')[0].split(',') })
    return groups

def showPretty(users, groups):
    table = PrettyTable(['users'] + [group[0] for group in list(groups)])
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
    parser = ArgumentParser()
    parser.add_argument("-m", "--mode", dest="mode",
                        help="working mode", metavar="table")
    parser.add_argument("-eu", "--excluded-users", dest="eu",
                        help="list of users which are excluded", metavar="root,user1,...")
    parser.add_argument("-eg", "--excluded-groups", dest="eg",
                        help="list of groups which are excluded", metavar="wheel,kvm,...")
    parser.add_argument("-iu", "--included-users", dest="iu",
                        help="list of users which you would like to include", metavar="root,user1,...")
    parser.add_argument("-ig", "--included-groups", dest="ig",
                        help="list of groups which you would like to include", metavar="wheel,kvm,...")
    args = parser.parse_args()
    eu, eg = [], []
    if args.eu:
        eu = args.eu.split(',')
    if args.eg:
        eg = args.eg.split(',')
    iu, ig = [], []
    if args.iu:
        iu = args.iu.split(',')
    if args.ig:
        ig = args.ig.split(',')
    if args.mode:
        mode = args.mode.strip()
        if mode == 'table':
            users = getUsers(excluded = eu)
            groups = getGroups(excluded = eg)
            showPretty(users, groups)
