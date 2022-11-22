import base64
import os
import random
import re
from pathlib import Path
from django.db import connection
import coder

BASE_DIR = Path(__file__).resolve().parent.parent


def user_exist(id, pwd):
    # todo 用户登录，返回为None则不存在，否则返回用户昵称
    return "xing"


def poster_exist(id, pwd):
    # todo 跑腿登录，返回为None则不存在，否则返回用户昵称
    return "Xing"


def manager_exist(id, pwd):
    # todo 跑腿登录，返回为None则不存在，否则返回用户昵称
    return "kao"


def poster_get_order(id, pwd):
    # todo 获取跑腿人员分配到的订单，返回一个数组，数组内为订单信息
    pass
