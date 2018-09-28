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
from multiprocessing import *
import sys
import signal
import traceback
import time


class Dic_sys(object):

    def __init__(self, c, db):
        self.__c = c
        self.__db = db

    # 注册操作
    def register(self, data):
        l = data[1:].split()
        name = l[0]
        pwd = l[1]
        cursor = self.__db.cursor()
        sql = "select * from user where name='%s'" % name
        cursor.execute(sql)
        r = cursor.fetchone()
        if r is not None:
            self.__c.send(b'exists')
            return
        sql = "insert into user(name,password) values('%s','%s')" % (name, pwd)
        try:
            cursor.execute(sql)
            self.__db.commit()
            self.__c.send(b'ok')
        except:
            self.__db.rollback()
            self.__c.send(b'failed')
            return
        else:
            print('%s注册成功' % name)

    # 登录
    def login(self, data):
        l = data[1:].split()
        name = l[0]
        pwd = l[1]
        cursor = self.__db.cursor()
        sql = "select * from user where name='%s' and password='%s'" % (name, pwd)
        cursor.execute(sql)
        r =cursor.fetchone()
        if r is None:
            self.__c.send('用户名或密码不正确'.encode())
        else:
            self.__c.send(b'ok')

    # 查词
    def look_up(self, data):
        l = data[1:].split()
        name = l[0]
        word = l[1]
        cursor = self.__db.cursor()
        def insert_history():
            tm = time.ctime()
            sql = "insert into history(name,word,time) values('%s','%s','%s')" % (name, word, tm)
            try:
                cursor.execute(sql)
                self.__db.commit()
            except:
                self.__db.rollback()
                return
        try:
            f = open('dic.txt', 'rb')
        except:
            self.__c.send('服务端异常'.encode())
            return
        while 1:
            line = f.readline().decode()
            w = line.split()[0]
            if (not line) or w > word:
                self.__c.send('未找到该单词'.encode())
                break
            elif w == word:
                self.__c.send(b'ok')
                time.sleep(0.1)
                self.__c.send(line.encode())
                insert_history()
                break
        f.close()

    # 查询查词记录
    def check_history(self, data):
        name = data[1:]
        cursor = self.__db.cursor()
        try:
            sql = "select * from history where name='%s'" % name
            cursor.execute(sql)
            r =cursor.fetchall()
            if not r:
                self.__c.send('没有历史记录'.encode())
                return
            else:
                self.__c.send(b'ok')
        except:
            self.__c.send('数据库查询异常'.encode())
            return
        n = 0
        for i in r:
            n += 1
            if n >10:
                break
            time.sleep(0.1)
            msg = "%s  %s  %s" % (i[1], i[2], i[3])
            self.__c.send(msg.encode())
        time.sleep(0.1)
        self.__c.send(b'##')



def fun(c, db):
    dic = Dic_sys(c, db)
    while 1:
        data = c.recv(1024).decode()
        print('请求是：', data)
        # 根据判断客户端发来的信息来执行相应的操作
        if (not data) or data[0] == 'E':
            c.close()
            sys.exit(0)
        elif data[0] == 'R':
            dic.register(data)
        elif data[0] == 'L':
            dic.login(data)
        elif data[0] == 'S':
            dic.look_up(data)
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
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
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
        p = Process(target=fun, args=(connfd, db))
        p.daemon = 1
        p.start()


if __name__ == '__main__':
    main()
