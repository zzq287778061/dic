#!/usr/local/bin/python3
# /-*- coding:utf-8 -*-
'''
name: zzq
last_edited: 18-09-27
项目：
    电子词典服务端
    功能：
        1.将dic.txt文件存到mysql数据库中
        2.根据客户端请求的指令，来做出相应的回复
'''
from socket import *
import os
from multiprocessing import *
import sys
import signal
import traceback


class dic_sys(object):

    pass


def main():
    HOST = ''
    PORT = 8888
    ADDR = (HOST, PORT)
    s = socket()
    s.bind(ADDR)
    s.listen(8)
    dic = dic_sys()



if __name__ == '__main__':
    main()