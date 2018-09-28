#!/usr/local/bin/python3
# /-*- coding:utf-8 -*-
'''
name: zzq
last_edited: 18-09-27
项目：
    电子词典
'''
import re
import sys


def check_it(WORD):
    f = open('dic.txt')
    pattern = r'\S+'

    for line in f:
        if not line:
            break
        try:
            word = re.findall(pattern, line)[0]
        except Exception as e:
            print(e)
        if word == WORD:
            print(line)
            break
    else:
        print('未找到')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('please input like python3 dic.py about')
        raise
    check_it(sys.argv[1])