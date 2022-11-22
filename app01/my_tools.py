import base64
import os
import random
import re
from pathlib import Path
from django.db import connection
import coder
BASE_DIR = Path(__file__).resolve().parent.parent


def user_exist(id, pwd):
    # todo 用户登录，pwd = coder.decode(pwd,id)，返回为None则不存在
    pwd = coder.decode(pwd, id)
    pass


def poster_exist(id, pwd):
    # todo 跑腿登录，pwd = coder.decode(pwd,id)，返回为None则不存在
    pwd = coder.decode(pwd,id)
    pass


def manager_exist(id, pwd):
    # todo 跑腿登录，pwd = coder.decode(pwd,id)，返回为None则不存在
    pwd = coder.decode(pwd, id)
    pass
