#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Copyright (c) 2022 Maksim Perov <coder@frtk.ru>
#

from argparse import ArgumentParser
from prettytable import PrettyTable
import hashlib
import json

def getUsers(excluded = [], included = []):
    users = {}
    with open("/etc/passwd" , "r") as f:
        for line in f.readlines():
            splited = line.split(":")
            shell = splited[-1:][0].split('\n')[0].split('/')[-1:][0]
            homePath = splited[-2:][0].split('/')
            name = splited[0]
            if 'home' in homePath and shell in ['bash', 'sh']:
                if included and name in included:
                    users.update({name : [splited[2], splited[3]]})
                elif excluded and name not in excluded:
                    users.update({name : [splited[2], splited[3]]})
                elif included == [] and excluded == []:
                    users.update({name : [splited[2], splited[3]]})
    return users

def getGroups(excluded = [], included = []):
    groups = {}
    with open("/etc/group" , "r") as f:
        for line in f.readlines():
            _list = line.split(":")
            name = _list[0]
            participants = _list[3]
            if participants.strip() != '':
                if included and name in included:
                    groups.update({ (name, _list[2]) : participants.split('\n')[0].split(',') })
                elif excluded and name not in excluded:
                    groups.update({ (name, _list[2]) : participants.split('\n')[0].split(',') })
                elif included == [] and excluded == []:
                    groups.update({ (name, _list[2]) : participants.split('\n')[0].split(',') })
    return groups

def showPretty(users, groups, reducing = True):
    lng = [group[0] for group in list(groups)]
    if reducing:
        for group in groups:
            count_minus = 0
            for user in users:
                if not user in groups[group]:
                    count_minus += 1
            if len(users) == count_minus:
                lng.remove(group[0])
    table = PrettyTable(['users'] + lng)
    for user in users:
        marks = []
        for group in groups:
            if group[0] not in lng:
                continue
            if user in groups[group]:
                marks.append('+')
            else:
                marks.append('-')
        table.add_row([user] + marks)
    print(table)

def showPrettyUsers(users):
    table = PrettyTable(['users', 'UID', 'GID'])
    for user in users:
        table.add_row([user, users[user][0], users[user][1]])
    print(table)

def showPrettyGroups(groups):
    table = PrettyTable(['groups', 'GID'])
    for group in groups:
        table.add_row([group[0], group[1]])
    print(table)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-m", "--mode", dest="mode",
                        help="working mode. This argument is main!", metavar="table,user,group,hash")
    parser.add_argument("-eu", "--excluded-users", dest="eu",
                        help="list of users which are excluded", metavar="root,user1,...")
    parser.add_argument("-eg", "--excluded-groups", dest="eg",
                        help="list of groups which are excluded", metavar="wheel,kvm,...")
    parser.add_argument("-iu", "--included-users", dest="iu",
                        help="list of users which you would like to include", metavar="root,user1,...")
    parser.add_argument("-ig", "--included-groups", dest="ig",
                        help="list of groups which you would like to include", metavar="wheel,kvm,...")
    parser.add_argument("-r", "--reducing", action='store_true',
                        help="it allows to reduce table. This option deletes groups which don't have any participant.")
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
        reducing = args.reducing
        mode = args.mode.strip()
        if mode == 'table':
            users = getUsers(excluded = eu, included = iu)
            groups = getGroups(excluded = eg, included = ig)
            showPretty(users, groups, reducing = reducing)
        elif mode == 'user':
            users = getUsers(excluded = eu, included = iu)
            showPrettyUsers(users)
        elif mode == 'group':
            groups = getGroups(excluded = eg, included = ig)
            showPrettyGroups(groups)
        elif mode == 'hash':
            groups = getGroups(excluded = eg, included = ig)
            to_json = {}
            for group in groups:
                name = group[0]
                GID = group[1]
                to_json.update({ name : { "GID" : GID, "users" : groups[group]}})
            hashsum = hashlib.md5(json.dumps(to_json, sort_keys=True).encode('utf-8')).hexdigest()
            print(hashsum)
        else:
            parser.print_help()
    else:
        parser.print_help()
