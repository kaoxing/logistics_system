import json
import os
import sys

from django.http import JsonResponse
from django.shortcuts import render, redirect

current_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_directory)

import coder
import my_tools as tls

# python manage.py runserver
local = "http://127.0.0.1:8000/"


# Create your views here.
def home(request):
    """主页"""
    return render(request, "home.html")


def user_login(request):
    """用户登录"""
    if request.method == 'GET':
        return render(request, "user_login.html")
    # 获取接收到的账号和密码
    data = json.loads(request.body)
    user_data = []
    id = data.get("user")
    pwd = data.get("pwd")
    name = tls.user_exist(id, pwd)
    user_data.extend([id, pwd, name, False])
    if name is not None:
        user_data[1] = coder.encode(pwd, id)
        user_data[3] = True
    print(user_data)
    return JsonResponse({"data": user_data})


def poster_login(request):
    """跑腿登录"""
    if request.method == 'GET':
        return render(request, "poster_login.html")
    # 获取接收到的账号和密码
    data = json.loads(request.body)
    print(data)
    user_data = []
    id = data.get("user")
    pwd = data.get("pwd")
    name = tls.poster_exist(id, pwd)
    user_data.extend([id, pwd, name, False])
    if name is not None:
        user_data[1] = coder.encode(pwd, id)
        user_data[3] = True
    print(user_data)
    return JsonResponse({"data": user_data})


def manager_login(request):
    """后台登录"""
    if request.method == 'GET':
        return render(request, "manager_login.html")
    # 获取接收到的账号和密码
    data = json.loads(request.body)
    user_data = []
    id = data.get("user")
    pwd = data.get("pwd")
    name = tls.manager_exist(id, pwd)
    user_data.extend([id, pwd, name, False])
    if name is not None:
        user_data[1] = coder.encode(pwd, id)
        user_data[3] = True
    print(user_data)
    return JsonResponse({"data": user_data})


def poster_index(request):
    """跑腿主页"""
    if request.method == 'GET':
        data = request.GET
        id = data.get('id')
        if id is None:
            return redirect(local + "poster_login/")
        name = data.get('name')
        pwd = data.get('pwd')
        return render(request, "poster_index.html", {'name': name, 'id': id, 'pwd': pwd})
    data = json.loads(request.body)
    ope = data.get("ope")
    if ope == "配送":
        order_num = data.get("订单编号")
        tls.poster_deliver(order_num)
        return redirect(local + "poster_index/")
    ret_list = []
    id = data.get("id")
    ret_list = tls.poster_get_order(id)
    print(ret_list)
    return JsonResponse({"data": ret_list})


def poster_setting(request):
    """跑腿设置"""
    if request.method == 'GET':
        data = request.GET
        id = data.get('id')
        name = data.get('name')
        pwd = data.get('pwd')
        if id is None:
            return redirect(local + "poster_login/")
        return render(request, "poster_setting.html", {'name': name, 'id': id, 'pwd': pwd})
    # 接收到修改请求
    data = json.loads(request.body)
    id = data.get('id')
    rName = data.get('resultName')
    sPwd = data.get('sourcePwd')
    rPwd = data.get('resultPwd')
    ans = [tls.poster_change_info(id, rName, sPwd, rPwd), rName]
    pwd = tls.setting_get_poster_pwd(id)
    print("here")
    if ans[0]:
        pwd = coder.encode(pwd, id)
        ans.append(pwd)
        return JsonResponse({"data": ans})
    pwd = coder.encode(pwd, id)
    ans.append(pwd)
    return JsonResponse({"data": ans})


def user_index(request):
    """用户主页"""
    if request.method == 'GET':
        data = request.GET
        id = data.get('id')
        if id is None:
            return redirect(local + "user_login/")
        name = data.get('name')
        pwd = data.get('pwd')
        return render(request, "user_index.html", {'name': name, 'id': id, 'pwd': pwd})
    data = json.loads(request.body)
    ret_list = []
    id = data.get("id")
    pwd = data.get("pwd")
    ope = data.get("ope")
    if ope == "收货":
        order_num = data.get("订单编号")
        tls.user_receive(order_num)
        return JsonResponse({"data": "None"})
    ret_list = tls.user_get_order(id)
    print(ret_list)
    return JsonResponse({"data": ret_list})


def user_setting(request):
    """用户设置"""
    if request.method == 'GET':
        data = request.GET
        id = data.get('id')
        name = data.get('name')
        pwd = data.get('pwd')
        buyId = tls.user_get_buyId(id)
        if id is None:
            return redirect(local + "user_login/")
        return render(request, "user_setting.html", {'name': name, 'id': id, 'pwd': pwd, 'buyId': buyId})
    # 接收到修改请求
    data = json.loads(request.body)
    ret_list = []
    id = data.get('id')
    rName = data.get('resultName')
    sPwd = data.get('sourcePwd')
    rPwd = data.get('resultPwd')
    buyId = data.get("buyId")
    tls.user_change_buyId(id, buyId)
    ans = [tls.user_change_info(id, rName, sPwd, rPwd), rName]
    pwd = tls.setting_get_user_pwd(id)
    if ans[0]:
        pwd = coder.encode(pwd, id)
        ans.append(pwd)
        return JsonResponse({"data": ans})
    pwd = coder.encode(pwd, id)
    ans.append(pwd)
    return JsonResponse({"data": ans})


def manager_distribute(request):
    """后台分配"""
    if request.method == 'GET':
        data = request.GET
        id = data.get('id')
        name = data.get('name')
        pwd = data.get('pwd')
        if id is None:
            return redirect(local + "manager_login/")
        order_list = tls.manager_get_distribute()
        return render(request, "manager_distribute.html",
                      {'name': name, 'id': id, 'pwd': pwd, 'List': json.dumps(order_list)})
    # 接收到请求
    data = json.loads(request.body)
    ret_list = []
    id = data.get("id")
    pwd = data.get("pwd")
    pwd = coder.decode(pwd, id)
    ope = data.get("ope")
    name = data.get('name')
    order_num = data.get("order_num")
    if tls.manager_exist(id, pwd) is None:
        return redirect(local + "manager_login/")
    if ope == "退货":
        tls.manager_refund(order_num)
    elif ope == "分配":
        tls.manager_distribute()
    return JsonResponse({"data": None})


def manager_poster(request):
    """后台跑腿"""
    if request.method == 'GET':
        data = request.GET
        id = data.get('id')
        name = data.get('name')
        pwd = data.get('pwd')
        if id is None:
            return redirect(local + "manager_login/")
        poster_list = tls.manager_get_poster()
        return render(request, "manager_poster.html",
                      {'name': name, 'id': id, 'pwd': pwd, 'List': json.dumps(poster_list)})
    # 接收到请求
    data = json.loads(request.body)
    id = data.get("id")
    pwd = data.get("pwd")
    ope = data.get("ope")
    poster_num = data.get("poster_num")
    pwd = coder.decode(pwd, id)
    if tls.manager_exist(id, pwd) is None:
        return redirect(local + "manager_login/")
    if ope == "删除":
        tls.manager_delete_poster(poster_num)
    if ope == "新增":
        PNum = data.get("PNum")
        PId = data.get("PId")
        PCall = data.get("PCall")
        PMail = data.get("PMail")
        PName = data.get("PName")
        tls.manager_new_poster(PNum, PName, PId, PCall, PMail)
    return JsonResponse({"data": None})


def map(request):
    if request.method == 'GET':
        return render(request, "map.html")
    data = json.loads(request.body)
    ret_list = []
    id = data.get("user")
    pwd = data.get("pwd")
    ret_list = tls.user_get_order(id, pwd)
    return JsonResponse({"data": ret_list})
