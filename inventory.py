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

def getGroups(excluded = [], included = [], excludedUsers = []):
    groups = {}
    with open("/etc/group" , "r") as f:
        for line in f.readlines():
            _list = line.split(":")
            name = _list[0]
            participants = _list[3]
            if participants.strip() != '':
                users = sorted(participants.split('\n')[0].split(','))
                for user in excludedUsers:
                    if user in users:
                        users.remove(user)
                if included and name in included:
                    groups.update({ name : { 'GID' : _list[2], 'users' : users }})
                elif excluded and name not in excluded:
                    groups.update({ name : { 'GID' : _list[2], 'users' : users }})
                elif included == [] and excluded == []:
                    groups.update({ name : { 'GID' : _list[2], 'users' : users }})
    return groups

def showPretty(users, groups, reducing = True):
    lng = [group for group in list(groups)]
    lng = sorted(lng)
    if reducing:
        for group in groups:
            count_minus = 0
            for user in users:
                if not user in groups[group]['users']:
                    count_minus += 1
            if len(users) == count_minus:
                lng.remove(group)
    table = PrettyTable(['users'] + lng)
    for user in users:
        marks = []
        for group in sorted(groups):
            if group not in lng:
                continue
            if user in groups[group]['users']:
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
        table.add_row([group, groups[group]['GID']])
    print(table)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-m", "--mode", dest="mode",
                        help="working mode. This argument is main!", metavar="table or user or group")
    parser.add_argument("-gh", "--get-hash", dest="hash",
                        help="getting of hash. This is alternative argument to main!", metavar="all or group or user")
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
    parser.add_argument("-d", "--debug", action='store_true',
                        help="this option enables debug mode")
    args = parser.parse_args()
    debug = args.debug
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
        else:
            parser.print_help()
    elif args.hash:
        mode = args.hash.strip()
        if mode == 'all':
            groups = getGroups(excluded = eg, included = ig, excludedUsers = eu)
            if debug:
                print(json.dumps(groups, indent=4, sort_keys=True))
            hashsum = hashlib.md5(json.dumps(groups, sort_keys=True).encode('utf-8')).hexdigest()
            print(hashsum)
        elif mode == 'group':
            groups = getGroups(excluded = eg, included = ig)
            to_json = {}
            for group in groups:
                name = group
                GID = groups[group]['GID']
                to_json.update({ name : GID })
            hashsum = hashlib.md5(json.dumps(to_json, sort_keys=True).encode('utf-8')).hexdigest()
            print(hashsum)
        elif mode == 'user':
            users = getUsers(excluded = eu, included = iu)
            hashsum = hashlib.md5(json.dumps(users, sort_keys=True).encode('utf-8')).hexdigest()
            print(hashsum)
    else:
        parser.print_help()
