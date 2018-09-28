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

import pymysql
import re

f = open('dic.txt')
db = pymysql.connect('localhost', 'root', 'zzqzzq123456', 'dic_project')

cursor = db.connect()
for line in f:
    try:
        l = re.split(r'[ ]+', line)
        word = l[0]
        meaning = ' '.join(l[1:])
    except:
        pass
    sql = 'insert into words(word,meaning) values("%s","%s")' % (word, meaning)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
f.close()


