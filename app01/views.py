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
    pwd = coder.encode(pwd, id)
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
    pwd = coder.encode(pwd, id)
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
    pwd = coder.encode(pwd, id)
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
        return redirect(local + "user_index/")
    ret_list = tls.user_get_order(id)
    return JsonResponse({"data": ret_list})


def user_setting(request):
    """用户设置"""
    if request.method == 'GET':
        data = request.GET
        id = data.get('id')
        name = data.get('name')
        pwd = data.get('pwd')
        if id is None:
            return redirect(local + "user_login/")
        return render(request, "user_setting.html", {'name': name, 'id': id, 'pwd': pwd})
    # 接收到修改请求
    data = json.loads(request.body)
    ret_list = []
    id = data.get("id")
    pwd = data.get("pwd")
    ope = data.get("ope")
    ans = [tls.user_change_info(id, rName, sPwd, rPwd), rName]
    pwd = tls.setting_get_user_pwd(id)
    if ans[0]:
        pwd = coder.encode(pwd, id)
        ans.append(pwd)
        return JsonResponse({"data": ans})
    pwd = coder.encode(pwd, id)
    ans.append(pwd)
    return JsonResponse({"data": ans})


def manager_order(request):
    """后台订单"""
    if request.method == 'GET':
        data = request.GET
        id = data.get('id')
        name = data.get('name')
        pwd = data.get('pwd')
        if id is None:
            return redirect(local + "manager_login/")
        return render(request, "manager_order.html.html", {'name': name, 'id': id, 'pwd': pwd})
    # 接收到请求
    data = json.loads(request.body)
    id = data.get('id')
    rName = data.get('resultName')
    sPwd = data.get('sourcePwd')
    rPwd = data.get('resultPwd')
    ans = [tls.user_change_info(id, rName, sPwd, rPwd), rName]
    pwd = tls.setting_get_user_pwd(id)
    if ans[0]:
        pwd = coder.encode(pwd, id)
        ans.append(pwd)
        return JsonResponse({"data": ans})
    pwd = coder.encode(pwd, id)
    ans.append(pwd)
    return JsonResponse({"data": ans})


def map(request):
    if request.method == 'GET':
        return render(request, "map.html")
    data = json.loads(request.body)
    ret_list = []
    id = data.get("user")
    pwd = data.get("pwd")
    ret_list = tls.user_get_order(id, pwd)
    return JsonResponse({"data": ret_list})
