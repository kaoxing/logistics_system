import base64
import os
import random
import re
from pathlib import Path
from django.db import connection

import coder

BASE_DIR = Path(__file__).resolve().parent.parent

#   例子，该方法在数据库中寻找用户
# def user_exist(id, pwd):
#    cursor = connection.cursor()
#    sql = "select * from shopper_table where shopper_num='{}'".format(id)  #sql语句
#    cursor.execute(sql)    #执行sql
#    rows = cursor.fetchall()   #获取执行结果rows,可以打印出来看看
#    if len(rows) != 0 and rows[0][2] == pwd:
#        return rows[0][1]
#    return None


def user_exist(id, pwd):
    # todo 用户登录，返回为None则不存在，否则返回用户昵称
    cursor = connection.cursor()
    sql = "select * from 用户信息表 where 用户_账号='{}'".format(id)  # sql语句
    cursor.execute(sql)  # 执行sql
    rows = cursor.fetchall()  # 获取执行结果rows
    print(rows) # 下标从0开始
    if len(rows) != 0 and rows[0][1] == pwd:
         str = rows[0][3].rstrip() # 去除串结尾空格
         return str
    return None

# user_exist test
# id = 'yh2014001'
# pwd = 'yh2014001'
# use_name=user_exist(id, pwd)
# print(use_name,'name')



def poster_exist(id, pwd):
    # todo 跑腿登录，返回为None则不存在，
    cursor = connection.cursor()
    return None


def manager_exist(id, pwd):
    # todo 后台登录，返回为None则不存在，否则返回用户昵称
    cursor = connection.cursor()
    return "kao"


def poster_get_order(id, pwd):
    # todo 获取跑腿人员分配到的订单，返回一个数组，数组内为订单信息
    pass


