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
    if len(rows) != 0 and rows[0][1] == pwd:
        str = rows[0][3].rstrip()  # 去除串结尾空格
        return str
    return None


# user_exist test
# id = 'yh2014001'
# pwd = 'yh2014001'
# use_name=user_exist(id, pwd)
# print(use_name,'name')


def poster_exist(id, pwd):
    # todo 跑腿登录，返回为None则不存在，否则返回跑腿昵称
    cursor = connection.cursor()
    sql = "select * from 跑腿人员信息表 where 跑腿_账号='{}'".format(id)  # sql语句
    cursor.execute(sql)  # 执行sql
    rows = cursor.fetchall()  # 获取执行结果rows
    if len(rows) != 0 and rows[0][6] == pwd:
        str = rows[0][1].rstrip()  # 去除串结尾空格
        return str
    return None


# poster_exist test
# id = 'pt2014001'
# pwd = 'pt2014001'
# use_name=poster_exist(id, pwd)
# print(use_name,'name')

def manager_exist(id, pwd):
    # todo 后台登录，返回为None则不存在，否则返回用户昵称
    cursor = connection.cursor()
    sql = "select * from 用户信息表 where 用户_账号='{}'".format(id)  # sql语句
    cursor.execute(sql)  # 执行sql
    rows = cursor.fetchall()  # 获取执行结果rows
    if len(rows) != 0 and rows[0][1] == pwd:
        str = rows[0][3].rstrip()  # 去除串结尾空格
        return str
    return None


# manager_exist test
# id = 'yh2014001'
# pwd = 'yh2014001'
# use_name=manager_exist(id, pwd)
# print(use_name,'name')

def poster_get_order(id):
    # todo 获取跑腿人员分配到的订单，返回一个数组，数组为订单信息
    cursor = connection.cursor()
    sql = "select * from order_poster_view where 配送_工号 = '{}'".format(id)
    print(sql)
    cursor.execute(sql)
    rows = cursor.fetchall()
    list = []
    for row in rows:
        dic = {
            "工号": row[0],
            "订单编号": row[2],
            '驿站编号': row[3],
            "收件电话": row[4],
            '是否退货': row[5],
            "是否签收": row[6]
        }
        list.append(dic)
    return list

# poster_get_order test
# id = 'pt2014001'
# pwd = 'pt2014001'
# list=poster_get_order(id, pwd)
# print(list)


def poster_deliver(order_num):
    # todo 订单配送,参数位订单编号，要求若配送状态为"还未配送"则更新为”正在配送“，若为”正在配送“则更新为“已经送达”
    pass
