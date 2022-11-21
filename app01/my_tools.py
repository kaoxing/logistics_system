import base64
import os
import random
import re
from pathlib import Path
from django.db import connection

BASE_DIR = Path(__file__).resolve().parent.parent


def user_exist(id, pwd):
    # 用户登录，pwd = coder.decode(pwd,id)，返回为None则不存在
    pass
    pass


def poster_exist(id, pwd):
    pass


def manager_exist(id, pwd):
    pass
