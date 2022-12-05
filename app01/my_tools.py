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


def poster_get_order(id):
    # todo 获取跑腿人员分配到的订单，返回一个数组，数组为订单信息
    cursor = connection.cursor()
    sql = "select * from order_poster_view where 配送_工号 = '{}'".format(id)
    # print(sql)
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


def poster_deliver(order_num):
    # todo 订单配送,参数位订单编号，要求若配送状态为"还未配送"则更新为”正在配送“，若为”正在配送“则更新为“已经送达”
    pass


def poster_change_info(id, rName, sPwd, rPwd):
    # todo 跑腿账号信息修改，参数为跑腿账号，跑腿要改为的名字，原密码，要改为的密码，
    #  要求先改名，此时不检验密码是否正确，再改密码，此时需要先确认原密码正确，再改密码，若要改为的密码为空，则不做修改
    cursor = connection.cursor()
    sql = ""  # 改名
    cursor.execute(sql)
    if len(rPwd) == 0:  # 若要改为的密码为空，则直接返回True不做修改
        return True
    sql = ""  # 验证原密码
    cursor.execute(sql)
    rows = cursor.fetchall()
    if len(rows) == 0:  # 若原密码错误，返回False
        return False
    sql = ""  # 修改密码
    cursor.execute(sql)
    return True  # 成功修改完密码后返回True


def setting_get_poster_pwd(id):
    # todo 通过跑腿账号获取跑腿账号密码,要求返回获取到的密码
    pass


def user_get_order(id):
    # todo 获取用户的订单，返回一个数组，数组为订单信息，类似poster_get_order
    pass


def user_change_info(id, rName, sPwd, rPwd):
    # todo 用户账号信息修改，参数为用户账号，用户要改为的名字，原密码，要改为的密码，
    #  要求先改名，此时不检验密码是否正确，再改密码，此时需要先确认原密码正确，再改密码，若要改为的密码为空，则不做修改
    pass