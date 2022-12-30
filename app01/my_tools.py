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


# ok
# print(user_exist('yh2014010','yh2014010'))
# print(user_exist('yh2014010','000000000'))


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


# ok
# print(poster_exist('pt2014010','pt2014010'))#账号密码正确
# print(poster_exist('pt2014010','000000000'))#账号密码错误


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


# tbc
# print(manager_exist('ad2014001','ad2014001'))#账号密码正确
# print(manager_exist('ad2014001','000000000'))#账号密码错误


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


# ok
# list1=poster_get_order('pt2014008')
# print(list1)


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


# ok
# print('testing here')
# poster_deliver('d221121077')

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


# ok
# poster_change_info('pt2014002','艾金凤new','pt2014002','pt2013002')
# print(poster_change_info('pt2014002','艾金凤','pt2014002','pt2014002'))

def setting_get_poster_pwd(id):
    # todo 通过跑腿账号获取跑腿账号密码,要求返回获取到的密码
    cursor = connection.cursor()
    sql = "select 跑腿_密码 from 跑腿人员信息表 where 跑腿_账号 = '{}'".format(id)
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows[0][0]


# ok
# print(setting_get_poster_pwd('pt2014003'))


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
            "收件电话": row[14],
        }
        list.append(dic)
    return list


# ok
# lst1=user_get_order('yh2014010')
# print(lst1)


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


# ok
# user_change_info('yh2014003','王瑞new','yh2014003','yh2014000')#密码正确用例
# print(user_change_info('yh2014003','王瑞','000000000','yh2014003'))#密码错误用例

def user_receive(order_num):
    # todo 用户收货
    cursor = connection.cursor()
    sql = "select 订单_是否签收 from 订单表 where 订单_编号 = '{}'".format(order_num)
    cursor.execute(sql)
    rows = cursor.fetchall()
    if rows[0][0] == 'N':
        sql = "update 订单表 set 订单_是否签收 = 'Y' where 订单_编号 = '{}'".format(order_num)
        cursor.execute(sql)


# ok
# user_receive('d221121077')

def user_get_buyId(id):
    cursor = connection.cursor()
    sql = "select 用户_购买账号 from 用户信息表 where 用户_账号 = '{}'".format(id)
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows[0][0].rstrip()


# ok
# print(user_get_buyId('yh2014008'))


def user_change_buyId(id, buyId):
    cursor = connection.cursor()
    sql = "update 用户信息表 set 用户_购买账号= '{}'  where 用户_账号='{}'".format(buyId, id)
    cursor.execute(sql)


# ok
# user_change_buyId('yh2014004','gm2014004')

def setting_get_user_pwd(id):
    # todo 查找用户密码
    cursor = connection.cursor()
    sql = "select 用户_密码 from 用户信息表 where 用户_账号 = '{}'".format(id)
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows[0][0]


# ok
# print(setting_get_user_pwd('yh2014008'))


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


# ok
# lst=manager_get_order()
# print(lst)


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
            "驿站编号": row[4],
            "账号": row[5],
            "密码": row[6],
        }
        list.append(dic)
    return list


# ok
# print(manager_get_poster())


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


# ok
# print(manager_get_distribute())


def manager_delete_order(order_id):
    cursor = connection.cursor()
    sql = "select * from 订单表 where 订单_编号='{}'".format(order_id)  # sql语句,查询此配送单是否存在
    cursor.execute(sql)  # 执行sql
    rows = cursor.fetchall()  # 获取执行结果rows
    print('rows:', rows)
    if len(rows) != 0:
        sql2 = "delete from 订单表 where 订单_编号='{}'".format(order_id)  # sql语句
        cursor.execute(sql2)  # 执行sql
        sql3 = "delete from 配送表 where 配送_订单编号='{}'".format(order_id)  # sql语句,删除配送表的对应订单
        cursor.execute(sql3)  # 执行sql
    return True


# ok
# print('testing here')
# print(manager_delete_order('0000000000'))#错误订单编号
# print(manager_delete_order('d221121087'))#正确订单编号


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


# ok
# print(manager_delete_poster('pt2014011'))


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


# ok
# print(manager_exist('ad2014004','ad2014004'))#账号密码均正确
# print(manager_exist('ad2014004','000000000'))#密码错误


def manager_refund(order_num):
    # todo 退货,参数位订单编号，将是否退货修改即可
    cursor = connection.cursor()
    sql = "select * from 订单表 where 订单_编号='{}'".format(order_num)  # sql语句，此检验订单是否存在
    cursor.execute(sql)  # 执行sql
    rows = cursor.fetchall()  # 获取执行结果rows
    if len(rows) != 0:
        sql = "update 订单表 set 订单_是否退货='Y' where 订单_编号='{}'".format(order_num)  # sql语句
        cursor.execute(sql)  # 执行sql
        return True
    else:
        return None  # 此订单不存在


# ok
# print(manager_refund('d221121077'))
# print(manager_refund('0000000000'))

def manager_new_poster(PNum, PName, PCardId, PCall, PMail, Pid, Ppsw):
    # todo 新增跑腿人员,参数为工号，名字，身份证号，电话，驿站,跑腿账号,跑腿密码
    cursor = connection.cursor()
    sql = "select * from 跑腿人员信息表 where 跑腿_工号='{}'".format(PNum)  # sql语句，此检验订单是否存在
    cursor.execute(sql)  # 执行sql
    rows = cursor.fetchall()  # 获取执行结果rows
    if len(rows) == 0:
        sql = "insert into 跑腿人员信息表 values('{}','{}','{}','{}','{}'," \
              "'{}','{}')".format(PNum, PName, PCardId, PCall, PMail, Pid, Ppsw)  # sql语句
        cursor.execute(sql)  # 执行sql
    return True


# ok
# print('testing here')
# print(manager_new_poster('pt2014011','张三','350181197206189011','11112340011','001','pt2014011','pt2014011'))


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


# ok
# manager_distribute()

def manager_modify_poster(PNum, PName, PCardId, PCall, PMail, Pid, Ppsw):
    # todo 修改跑腿人员信息,参数为工号，名字，身份证号，电话，驿站,账号,密码
    # 工号不会被修改，用工号查找然后修改即可
    cursor = connection.cursor()
    sql = "select * from 跑腿人员信息表 where 跑腿_工号='{}'".format(PNum)
    cursor.execute(sql)  # 执行sql
    rows = cursor.fetchall()  # 获取执行结果rows
    if len(rows) != 0:
        sql = "update 跑腿人员信息表 set 跑腿_姓名='{}',跑腿_身份证号='{}',跑腿_电话='{}',跑腿_驿站编号='{}',跑腿_账号='{}'," \
              "跑腿_密码='{}' where 跑腿_工号='{}'".format(PName, PCardId, PCall, PMail, Pid, Ppsw, PNum)  # sql语句
        print(sql)
        cursor.execute(sql)  # 执行sql
    return


# ok
# manager_modify_poster('pt2014011','张三','350181197206189011','12345678911','002','pt2014011','pt2014011')


def manager_modify_distribute(order_num, poster_num):
    # todo 修改订单分配人员，参数为订单号，要分配给的跑腿工号
    cursor = connection.cursor()
    sql = "select * from 订单表 where 订单_编号='{}'".format(order_num)  # sql语句，此检验订单是否存在
    cursor.execute(sql)  # 执行sql
    rows = cursor.fetchall()  # 获取执行结果rows
    if len(rows) != 0:
        sql = "select * from 跑腿人员信息表 where 跑腿_工号='{}'".format(poster_num)  # sql语句
        cursor.execute(sql)
        rows_ = cursor.fetchall();
        if len(rows_) != 0 and rows_[0][4] == rows[0][7]:
            sql = "update 配送表 set 配送_工号='{}' where 配送_订单编号='{}'".format(poster_num, order_num)  # sql语句
            cursor.execute(sql)  # 执行sql
            return True
        else:
            return None
    else:
        return None  # 此订单不存在


# ok
# print(manager_modify_distribute('0000000000','pt2014011'))#订单号不存在
# print(manager_modify_distribute('d221121108','pt2014011'))#订单号存在，但驿站不匹配
# print(manager_modify_distribute('d221121022','pt2014011'))#订单号存在，驿站匹配


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


# ok
# print(manager_get_mail())


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


# ok
# manager_new_mail('009','安徽大学','12345678911','117.181111','31.77777')

def manager_modify_mail(MNum, MAdd, MCall, MX, MY):
    # todo 修改驿站信息，驿站编号，驿站地址，驿站电话，经度和纬度
    # 驿站编号不会被修改，用编号查找然后修改即可
    cursor = connection.cursor()
    sql = "select * from 驿站信息表 where 驿站_编号='{}'".format(MNum)  # sql语句，此检验订单是否存在
    cursor.execute(sql)  # 执行sql
    rows = cursor.fetchall()  # 获取执行结果rows
    if len(rows) != 0:
        sql = "update 驿站信息表 set 驿站_地址='{}',驿站_电话='{}',驿站_经度='{}',驿站_纬度='{}' " \
              "where 驿站_编号='{}'".format(MAdd, MCall, MX, MY, MNum)  # sql语句
        cursor.execute(sql)  # 执行sql
    return


# ok
# manager_modify_mail('009','安徽省合肥市蜀山区九龙路安徽大学梅园','12345678911','117.00000','31.7000')

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


# ok
# manager_delete_mail('009')

def insert_order(order_num, number, mail_num, user_id, goods_name):
    # todo 向订单表中插入一条新数据，订单号，数量，驿站编码，用户购买账户id
    cursor = connection.cursor()
    sql = "insert into 订单表 values('{}', '{}', '{}', '{}', 'N', 'N', 'N', '{}', '无')" \
        .format(order_num, user_id, goods_name, number, mail_num)
    cursor.execute(sql)
    pass


def get_mails():
    # todo 获取当前所有驿站的编号，返回编号数组
    cursor = connection.cursor()
    sql = "select * from 驿站信息表"
    cursor.execute(sql)
    rows = cursor.fetchall()
    list = []
    # print(rows)
    for row in rows:
        list.append([row[0].rstrip(), row[1].rstrip()])
    mails_list = list
    ret_list = []
    for mail in mails_list:
        dic = {
            "value": mail[0],
            "label": mail[1],
        }
        ret_list.append(dic)
    return ret_list
