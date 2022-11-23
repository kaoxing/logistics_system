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
    ret_list = []
    id = data.get("user")
    pwd = data.get("pwd")
    tls.poster_get_order(id, pwd)
    # todo
    return JsonResponse({"data": ret_list})



