#!/usr/bin/env python3
# -*- coding: utf-8 -*-

TARGET_GROUPS = [ ]

if __name__ == "__main__":
    groups = []
    with open("/etc/group" , "r") as f:
        for line in f.readlines():
            groups.append(line.split(":")[0])
    print(groups)
