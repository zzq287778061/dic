#!/usr/local/bin/python3
# /-*- coding:utf-8 -*-
'''
name: zzq
last_edited: 18-09-27
项目：
    电子词典客户端
    功能：
        1.注册，登录，退出
        2.登录后，可以查单词，可以查看查词历史记录，退出到上一界面
'''
from socket import *
import sys
import getpass


class Dic_client(object):

    def __init__(self,s):
        self.__s = s

    def register(self):
        while 1:
            name = input('用户名：')
            password = getpass.getpass('密码：')
            password1 = getpass.getpass('确认密码：')
            if (' ' in name) or (' ' in password):
                print('用户名密码不能存在空格')
                continue
            if password != password1:
                print('两次密码不一样')
                continue
            msg = 'R'+name+' '+password
            # 发送请求
            self.__s.send(msg.encode())
            # 接受回复
            data = self.__s.recv(1024).decode()
            if data == 'ok':
                print('注册成功')
                return name
            elif data == 'exists':
                print('用户名已存在')
                return 1
            else:
                return 1

    def do_login(self):
        name = input('请输入用户名：')
        pwd = getpass.getpass('密码：')
        msg = 'L'+name+' '+pwd
        self.__s.send(msg.encode())
        data = self.__s.recv(1024).decode()
        if data == 'ok':
            return name
        else:
            print(data)
            return 1

    def login(self,name):
        while 1:
            menu2()
            cmd2 = input('请输入选择：')
            if cmd2 not in ['1', '2', '3']:
                print('尚未有此功能，系统完善中，敬请期待')
                continue
            elif cmd2 == '1':
                self.look_up()
            elif cmd2 == '2':
                pass
            elif cmd3 == '3':
                return


def menu2():
    print('+----尊敬的用户，欢迎您的使用---+')
    print('+   1 查词                  +')
    print('+   2 查看历史记录           +')
    print('+   3 返回上一界面           +')
    print('+--------------------------+')



def menu():
    print('+-----欢迎使用英英字典v1.0----+')
    print('+   1 注册                  +')
    print('+   2 登录                  +')
    print('+   3 退出                  +')
    print('+--------------------------+')

def main():
    if len(sys.argv) < 3:
        print('tpye error! please input like'
              ' python3 dic_client 127.0.0.1 8888')
        raise
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST, PORT)
    # 创建套接字
    s =socket()
    s.connect(ADDR)
    dic_client = Dic_client(s)
    while 1:
        menu()
        cmd = input('请输入选择：')
        if cmd not in ['1', '2', '3']:
            print('尚未有此功能，系统完善中，敬请期待')
            continue
        elif cmd == '1':
            name = dic_client.login()
            if name != 1:
                dic_client.login(name)
            else:
                print('注册失败')
        elif cmd == '2':
            name = dic_client.do_login()
            if name != 1:
                print('登录成功')
                dic_client.login(name)
            else:
                print('登录失败')
        elif cmd == '3':
            print('欢迎下次使用')
            s.send(b'E')
            s.close()
            break



if __name__ == '__main__':
    main()