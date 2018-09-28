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
import pymysql
import os
from multiprocessing import *
import sys
import signal
import traceback


class Dic_sys(object):

    def __init__(self,c,db):
        self.__c = c
        self.__db = db

    def register(self,data):
        pass

    def login(self,data):
        pass

    def search(self,data):
        pass

    def check_history(self,data):
        pass


def fun(c,db):
    dic = Dic_sys(c,db)
    while 1:
        data = c.recv(1024).decode()
        print('请求是：', data)
        if (not data) or data[0] == 'E':
            c.close()
            sys.exit(0)
        elif data[0] == 'R':
            dic.register(data)
        elif data[0] == 'L':
            dic.login(data)
        elif data[0] == 'S':
            dic.search(data)
        elif data[0] == 'H':
            dic.check_history(data)



def main():
    # 创建套接字
    HOST = ''
    PORT = 8888
    ADDR = (HOST, PORT)
    s = socket()
    s.bind(ADDR)
    s.listen(8)
    # 数据库连接
    db = pymysql.connect('localhost', 'root', 'zzqzzq123456', 'dic_project')
    # 忽略子进程退出
    signal.signal(signal.SIG_IGN, signal.SIGCHLD)
    while 1:
        try:
            connfd, addr = s.accept()
            print('connected with ', addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit('服务器退出')
        except Exception as e:
            traceback.print_exc()
            continue
        # 创建子进程来处理客户端请求
        p = Process(target=fun,args=(coonfd,db))
        p.daemon = 1
        p.start()




if __name__ == '__main__':
    main()