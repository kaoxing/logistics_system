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
            "订单编号": row[2].rstrip(),
            '驿站编号': row[3].rstrip(),
            "收件电话": row[4].rstrip(),
            '是否退货': row[5].rstrip(),
            "是否签收": row[6].rstrip(),
            "物流状态": row[7].rstrip(),
            "驿站地址": row[8].rstrip(),
            "驿站经度": row[9].rstrip(),
            "驿站纬度": row[10].rstrip()
        }
        list.append(dic)
    return list


def poster_deliver(order_num):
    # todo 订单配送,参数位订单编号，要求若配送状态为"还未配送"则更新为”正在配送“，若为”正在配送“则更新为“已经送达”
    cursor = connection.cursor()
    sql = "select 配送_状态 from 配送表 where 配送_订单编号 = '{}'".format(order_num)
    cursor.execute(sql)
    rows = cursor.fetchall()
    print(rows[0][0])
    print("!!!")
    if rows[0][0] == 'N':
        sql = "update 配送表 set 配送_状态 = 'Y' where 配送_订单编号 = '{}'".format(order_num)
        cursor.execute(sql)
    elif rows[0][0] == 'Y':
        sql = "update 配送表 set 配送_状态 = 'P' where 配送_订单编号 = '{}'".format(order_num)
        cursor.execute(sql)


def poster_change_info(id, rName, sPwd, rPwd):
    # todo 跑腿账号信息修改，参数为跑腿账号，跑腿要改为的名字，原密码，要改为的密码，
    #  要求先改名，此时不检验密码是否正确，再改密码，此时需要先确认原密码正确，再改密码，若要改为的密码为空，则不做修改
    cursor = connection.cursor()
    sql = "update 跑腿人员信息表 set 跑腿_姓名='{}' where 跑腿_账号='{}'".format(rName, id)  # 改名
    cursor.execute(sql)
    if len(rPwd) == 0:  # 若要改为的密码为空，则直接返回True不做修改
        return True
    sql = "select * from 跑腿人员信息表 where 跑腿_密码 = '{}' ".format(sPwd)  # 验证原密码
    cursor.execute(sql)
    rows = cursor.fetchall()
    if len(rows) == 0:  # 若原密码错误，返回False
        return False
    sql = "update 跑腿人员信息表 set 跑腿_密码= '{}'  where 跑腿_账号='{}'".format(rPwd, id)  # 修改密码
    cursor.execute(sql)
    return True  # 成功修改完密码后返回True


def setting_get_poster_pwd(id):
    # todo 通过跑腿账号获取跑腿账号密码,要求返回获取到的密码
    cursor = connection.cursor()
    sql = "select 跑腿_密码 from 跑腿人员信息表 where 跑腿_账号 = '{}'".format(id)
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows[0][0]


def user_get_order(id):
    # todo 获取用户的订单，返回一个数组，数组为订单信息，类似poster_get_order
    cursor = connection.cursor()
    sql = "select * from user_view where 账号 = '{}'".format(id)
    cursor.execute(sql)
    rows = cursor.fetchall()
    list = []
    for row in rows:
        dic = {
            "订单编号": row[0],
            '物品名称': row[3],
            "物品数量": row[4],
            '是否退货': row[5],
            "是否签收": row[6],
            "配送状态": row[7],
            "负责跑腿人员": row[8],
            "跑腿人员电话": row[9],
            "驿站编号": row[10],
            "驿站电话": row[11],
            "驿站经度": row[12],
            "驿站纬度": row[13],
        }
        list.append(dic)
    return list


def user_change_info(id, rName, sPwd, rPwd):
    # todo 用户账号信息修改，参数为用户账号，用户要改为的名字，原密码，要改为的密码，
    #  要求先改名，此时不检验密码是否正确，再改密码，此时需要先确认原密码正确，再改密码，若要改为的密码为空，则不做修改
    cursor = connection.cursor()
    sql = "update 用户信息表 set 用户_姓名='{}' where 用户_账号='{}'".format(rName, id)  # 改名
    cursor.execute(sql)

    if len(rPwd) == 0:  # 若要改为的密码为空，则直接返回True不做修改
        return True
    sql = "select * from 用户信息表 where 用户_密码 = '{}' ".format(sPwd)  # 验证原密码
    cursor.execute(sql)
    rows = cursor.fetchall()
    if len(rows) == 0:  # 若原密码错误，返回False
        return False

    sql = "update 用户信息表 set 用户_密码= '{}'  where 用户_账号='{}'".format(rPwd, id)  # 修改密码
    cursor.execute(sql)
    return True  # 成功修改完密码后返回True


def user_receive(order_num):
    # todo 用户收货
    cursor = connection.cursor()
    sql = "select 订单_是否签收 from 订单表 where 订单_编号 = '{}'".format(order_num)
    cursor.execute(sql)
    rows = cursor.fetchall()
    if rows[0][0] == 'N':
        sql = "update 订单表 set 订单_是否签收 = 'Y' where 订单_编号 = '{}'".format(order_num)
        cursor.execute(sql)


def user_get_buyId(id):
    cursor = connection.cursor()
    sql = "select 用户_购买账号 from 用户信息表 where 用户_账号 = '{}'".format(id)
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows[0][0].rstrip()


def user_change_buyId(id, buyId):
    cursor = connection.cursor()
    sql = "update 用户信息表 set 用户_购买账号= '{}'  where 用户_账号='{}'".format(buyId, id)
    cursor.execute(sql)


def setting_get_user_pwd(id):
    # todo 查找用户密码
    cursor = connection.cursor()
    sql = "select 用户_密码 from 用户信息表 where 用户_账号 = '{}'".format(id)
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows[0][0]


def manager_get_order():
    cursor = connection.cursor()
    sql = "select * from 订单表"
    cursor.execute(sql)
    print(sql)
    rows = cursor.fetchall()
    print(rows)
    list = []
    for row in rows:
        dic = {
            "订单编号": row[0],
            "购买账号": row[1],
            '物品名称': row[2],
            "物品数量": row[3],
            '是否退货': row[4],
            "是否签收": row[5],
            "驿站编号": row[6],
            "收件电话": row[7]
        }
        list.append(dic)
    return list


def manager_get_poster():
    # todo 可以加一点驿站信息
    cursor = connection.cursor()
    sql = "select * from 跑腿人员信息表"
    cursor.execute(sql)
    # print(sql)
    rows = cursor.fetchall()
    # print(rows)
    list = []
    for row in rows:
        dic = {
            "工号": row[0],
            "姓名": row[1],
            "身份证号": row[2],
            "电话": row[3],
            "驿站编号": row[4]
        }
        list.append(dic)
    return list


def manager_get_distribute():
    cursor = connection.cursor()
    sql = "select * from user_view"
    cursor.execute(sql)
    # print(sql)
    rows = cursor.fetchall()
    # print(rows)
    list = []
    for row in rows:
        dic = {
            "订单编号": row[0],
            "用户账号": row[1],
            '物品名称': row[3],
            "物品数量": row[4],
            '是否退货': row[5],
            "是否签收": row[6],
            "配送状态": row[7],
            "负责跑腿人员": row[8],
            "跑腿人员电话": row[9],
            "驿站编号": row[10],
            "驿站电话": row[11],
            "驿站经度": row[12],
            "驿站纬度": row[13],
            "是否分配": row[14],
        }
        list.append(dic)
    return list


def manager_delete_order(order_id):
    cursor = connection.cursor()
    sql1 = "select * from 配送表 where 配送_订单编号='{}'".format(order_id)  # sql语句,查询此配送单是否存在
    cursor.execute(sql1)  # 执行sql
    rows = cursor.fetchall()  # 获取执行结果rows
    if len(rows) != 0:
        sql2 = "delete from 配送表 where 配送_订单编号='{}'".format(order_id)  # sql语句
        cursor.execute(sql2)  # 执行sql
        return True
    else:
        return None  # 订单不存在


def manager_delete_poster(poster_id):
    cursor = connection.cursor()
    sql1 = "select * from 跑腿人员信息表 where 跑腿_工号='{}'".format(poster_id)  # sql语句,查询此跑腿是否存在
    cursor.execute(sql1)  # 执行sql
    rows = cursor.fetchall()  # 获取执行结果rows
    if len(rows) != 0:
        sql2 = "delete from 跑腿人员信息表 where 跑腿_工号='{}'".format(poster_id)  # sql语句
        cursor.execute(sql2)  # 执行sql
        return True
    else:
        return None  # 跑腿不存在


def manager_exist(id, pwd):
    # todo 管理员登录，返回为None则不存在，否则返回用户昵称
    cursor = connection.cursor()
    sql = "select * from 管理员 where 管理员_账号='{}'".format(id)  # sql语句
    cursor.execute(sql)  # 执行sql
    print(sql)
    rows = cursor.fetchall()  # 获取执行结果rows
    print(rows[0][1], pwd)
    print(rows[0][1] == pwd)
    if len(rows) != 0 and rows[0][1] == pwd:
        str = rows[0][2].rstrip()  # 去除串结尾空格
        return str
    return None


def manager_refund(order_num):
    # todo 退货,参数位订单编号，将是否退货修改即可
    cursor = connection.cursor()
    sql = "select * from 订单表 where 订单_编号='{}'".format(order_num)  # sql语句，此检验订单是否存在
    cursor.execute(sql)  # 执行sql
    rows = cursor.fetchall()  # 获取执行结果rows
    if len(rows) != 0 :
        sql = "update 订单表 set 订单_是否退货='Y' where 订单_编号='{}'".format(order_num)  # sql语句
        cursor.execute(sql)  # 执行sql
        return True
    else:
        return None # 此订单不存在


def manager_new_poster(PNum, PName, PCardId, PCall, PMail,Pid,Ppsw):
    # todo 新增跑腿人员,参数为工号，名字，身份证号，电话，驿站,跑腿账号,跑腿密码
    cursor = connection.cursor()
    sql = "select * from 跑腿人员信息表 where 跑腿_工号='{}'".format(PNum)  # sql语句，此检验订单是否存在
    cursor.execute(sql)  # 执行sql
    rows = cursor.fetchall()  # 获取执行结果rows
    if len(rows) == 0:
        sql = "insert into 跑腿人员信息表 values('{}','{}','{}','{}','{}'," \
              "'{}','{}')".format(PNum,PName,PCardId,PCall,PMail,Pid,Ppsw)  # sql语句
        cursor.execute(sql)  # 执行sql
    return True


def manager_distribute():
    # todo 对所有未分配订单进行分配
    cursor = connection.cursor()

    lists = [[] for i in range(1000)]
    num = [0 for i in range(1000)]
    cur = [0 for i in range(1000)]

    sql = "select * from 跑腿人员信息表"
    cursor.execute(sql)
    rows = cursor.fetchall()

    print(len(rows))

    for row in rows:
        lists[int(row[4])].append(row[0])
        num[int(row[4])] += 1

    sql = "select * from 订单表 where 订单_是否分配 = 'N'"
    cursor.execute(sql)
    rows = cursor.fetchall()

    for row in rows:
        station = int(row[7])
        sql = "insert into 配送表 values('{}', '{}', '{}')".format(row[0], lists[station][cur[station]], "N")
        cursor.execute(sql)
        print(station)
        print(sql)
        cur[station] += 1
        if cur[station] == num[station]:
            cur[station] = 0;

    sql = "update 订单表 set 订单_是否分配 = 'Y'"
    cursor.execute(sql)

    return


def manager_modify_poster(PNum, PName, PCardId, PCall, PMail,Pid,Ppsw):
    # todo 修改跑腿人员信息,参数为工号，名字，身份证号，电话，驿站,账号,密码
    # 工号不会被修改，用工号查找然后修改即可
    cursor = connection.cursor()
    sql = "select * from 跑腿人员信息表 where 跑腿_工号='{}'".format(PNum)  # sql语句，此检验订单是否存在
    cursor.execute(sql)  # 执行sql
    rows = cursor.fetchall()  # 获取执行结果rows
    if len(rows) != 0:
        sql = "update 跑腿人员信息表 set 跑腿_姓名='{}',跑腿_身份证号='{}',跑腿_电话='{}',跑腿_驿站编号='{}',跑腿_账号='{}'," \
              "跑腿_密码='{}' where 跑腿_工号='{}'".format(PName, PCardId, PCall, PMail,Pid,Ppsw,PNum)  # sql语句
        cursor.execute(sql)  # 执行sql
    return


def manager_modify_distribute(order_num, poster_num):
    # todo 修改订单分配人员，参数为订单号，要分配给的跑腿工号
    cursor = connection.cursor()
    sql = "select * from 订单表 where 订单_编号='{}'".format(order_num)  # sql语句，此检验订单是否存在
    cursor.execute(sql)  # 执行sql
    rows = cursor.fetchall()  # 获取执行结果rows
    if len(rows) != 0:
        sql = "update 配送表 set 配送_工号='{}' where 配送_订单编号='{}'".format(poster_num,order_num)  # sql语句
        cursor.execute(sql)  # 执行sql
        return True
    else:
        return None  # 此订单不存在


def manager_get_mail():
    # todo 获取所有驿站信息，可参考manager_get_distribute()
    cursor = connection.cursor()
    sql = "select * from 驿站信息表"
    cursor.execute(sql)
    # print(sql)
    rows = cursor.fetchall()
    # print(rows)
    list = []
    for row in rows:
        dic = {
            "驿站编号": row[0].rstrip(),
            "驿站地址": row[1].rstrip(),
            '驿站电话': row[2].rstrip(),
            "驿站经度": row[3].rstrip(),
            '驿站纬度': row[4].rstrip()
        }
        list.append(dic)
    return list


def manager_new_mail(MNum, MAdd, MCall, MX, MY):
    # todo 新增驿站,驿站编号，驿站地址，驿站电话，经度和纬度
    cursor = connection.cursor()
    sql = "select * from 驿站信息表 where 驿站_编号='{}'".format(MNum)  # sql语句，此检验订单是否存在
    cursor.execute(sql)  # 执行sql
    rows = cursor.fetchall()  # 获取执行结果rows
    if len(rows) == 0:
        sql = "insert into 驿站信息表 values('{}','{}','{}','{}','{}')".format(MNum, MAdd, MCall, MX, MY)  # sql语句
        cursor.execute(sql)  # 执行sql
    return


def manager_modify_mail(MNum, MAdd, MCall, MX, MY):
    # todo 修改驿站信息，驿站编号，驿站地址，驿站电话，经度和纬度
    # 驿站编号不会被修改，用编号查找然后修改即可
    cursor = connection.cursor()
    sql = "select * from 驿站信息表 where 驿站_编号='{}'".format(MNum)  # sql语句，此检验订单是否存在
    cursor.execute(sql)  # 执行sql
    rows = cursor.fetchall()  # 获取执行结果rows
    if len(rows) != 0:
        sql = "update 驿站信息表 set 驿站_地址='{}',驿站_电话='{}',驿站_经度='{}',驿站_纬度='{}' " \
              "where 驿站_编号='{}'".format(MAdd, MCall, MX, MY,MNum)  # sql语句
        cursor.execute(sql)  # 执行sql
    return


def manager_delete_mail(mail_num):
    # todo 删除驿站，参数为驿站编号
    cursor = connection.cursor()
    sql1 = "select * from 驿站信息表 where 驿站_编号='{}'".format(mail_num)  # sql语句,查询此跑腿是否存在
    cursor.execute(sql1)  # 执行sql
    rows = cursor.fetchall()  # 获取执行结果rows
    if len(rows) != 0:
        sql2 = "delete from 驿站信息表 where 驿站_编号='{}'".format(mail_num)  # sql语句
        cursor.execute(sql2)  # 执行sql
    return


