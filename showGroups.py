#!/usr/bin/env python3
# -*- coding: utf-8 -*-

TARGET_GROUPS = [ ]

def getGroups():
    groups = []
    with open("/etc/group" , "r") as f:
        for line in f.readlines():
            groups.append(line.split(":")[0])
    return groups

if __name__ == "__main__":
    print(getGroups())
