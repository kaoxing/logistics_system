import json
import os
import sys

from django.http import JsonResponse
from django.shortcuts import render, redirect

current_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_directory)

import coder
import my_tools as tls
import my_ports as pts

# python manage.py runserver
local = "http://127.0.0.1:8000/"

# 约定好的外部接口密钥，此处是明文，传输时应当用coder.encoder()方法加密，加密的key也需要约定好，此处我用的是coderX
# 如果其余组没有加密模块，或加密方式不同，明文传输也不是不行，反正也没人看
portKey = "the_long_dark"


def port(request):
    """
    外部访问接口，访问地址为.../port/
    此处规定数据格式为json类型
    请求类型为POST
    数据体data={
        ope="",//具体操作类型，如为"buyOrder"则为获取数据库中订单内容
        portKey="",//密钥，在执行操作前，应当确定密钥是否正确，密钥应事先约定好，数据体中的portKey是加密后的结果
        load="",//实际装载数据
    }
    """
    if request.method != "POST":
        return JsonResponse({"info": "错误的调用方式!"})
    data = json.loads(request.body)
    ope = data.get("ope")
    key = data.get("portKey")
    load = data.get("load")
    print(data)
    if portKey != coder.decode(key, "coderX"):
        # 若密钥错误
        return JsonResponse({"info": "错误的密钥!"})
    if ope == "refund":
        # 接收到客服系统传来的退货数据
        order_num = data.get("order_num")
        tls.manager_refund(load.get("order_num"))
        return JsonResponse({"info": "成功接收"})
    elif ope == "buyOrder":
        # 接收到购买系统传来的订单数据
        order_num = data.get("ONO")
        number = data.get("ONUM")
        mail_num = data.get("OADERSS")
        user_id = data.get("UNO")
        tls.insert_order(order_num, number, mail_num, user_id)
        return JsonResponse({"info": "成功接收"})
    # elif ope == "":
    return JsonResponse({"info": "error"})


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
    poster_num = data.get("poster_num")
    print(data)
    if tls.manager_exist(id, pwd) is None:
        return redirect(local + "manager_login/")
    if ope == "退货":
        # tls.manager_refund(order_num)
        pts.post_something()
    elif ope == "分配":
        tls.manager_distribute()
    elif ope == "修改":
        tls.manager_modify_distribute(order_num, poster_num)
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
    print(data)
    if tls.manager_exist(id, pwd) is None:
        return redirect(local + "manager_login/")
    elif ope == "删除":
        tls.manager_delete_poster(poster_num)
    elif ope == "新增":
        PNum = data.get("PNum")
        PId = data.get("PId")
        PCall = data.get("PCall")
        PMail = data.get("PMail")
        PName = data.get("PName")
        tls.manager_new_poster(PNum, PName, PId, PCall, PMail)
    elif ope == "修改":
        PNum = data.get("PNum")
        PId = data.get("PId")
        PCall = data.get("PCall")
        PMail = data.get("PMail")
        PName = data.get("PName")
        tls.manager_modify_poster(PNum, PName, PId, PCall, PMail)
    return JsonResponse({"data": None})


def manager_mail(request):
    """后台驿站"""
    if request.method == 'GET':
        data = request.GET
        id = data.get('id')
        name = data.get('name')
        pwd = data.get('pwd')
        if id is None:
            return redirect(local + "manager_mail/")
        mail_list = tls.manager_get_mail()
        return render(request, "manager_mail.html",
                      {'name': name, 'id': id, 'pwd': pwd, 'List': json.dumps(mail_list)})
    # 接收到请求
    data = json.loads(request.body)
    id = data.get("id")
    pwd = data.get("pwd")
    ope = data.get("ope")
    mail_num = data.get("mail_num")
    pwd = coder.decode(pwd, id)
    print(data)
    if tls.manager_exist(id, pwd) is None:
        return redirect(local + "manager_login/")
    elif ope == "删除":
        tls.manager_delete_mail(mail_num)
    elif ope == "新增":
        MNum = data.get("MNum")
        MAdd = data.get("MAdd")
        MCall = data.get("MCall")
        MX = data.get("MX")
        MY = data.get("MY")
        tls.manager_new_mail(MNum, MAdd, MCall, MX, MY)
    elif ope == "修改":
        MNum = data.get("MNum")
        MAdd = data.get("MAdd")
        MCall = data.get("MCall")
        MX = data.get("MX")
        MY = data.get("MY")
        tls.manager_modify_mail(MNum, MAdd, MCall, MX, MY)
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
