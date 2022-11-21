import json
import os
import sys

from django.http import JsonResponse
from django.shortcuts import render

current_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_directory)

import coder
import my_tools as tls

# D:\anaconda\envs\database\python.exe manage.py runserver
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
        return render(request, "user_login.html")
    # 获取接收到的账号和密码
    data = json.loads(request.body)
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
        return render(request, "user_login.html")
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
