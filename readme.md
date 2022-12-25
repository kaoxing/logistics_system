python# 启动方法

### 确保终端进入manage.py文件目录中，执行以下
```
python(或者改成django所在解释器的python.exe路径) manage.py runserver
```
***
### 该项目所使用django版本为3.2
[官方文档](https://docs.djangoproject.com/zh-hans/3.0/)
***
### 如果有报错缺少相应Model则安装指定包即可
```
若缺少corsheads，则 pip install django-cors-headers
若缺少数据库连接相关，则 pip install psycopg2
若缺少加密模块，则 pip install Cryptography
```
***
### app01/my_tools.py
my_tools.py 里是所有需要实现的与数据库操作或数据处理有关的方法
***
### app01/coder.py
##### 方法 encode(source, key)
该方法将字符串source以字符串key作为密钥进行加密，返回加密后的字符串，密钥最长16位
##### 方法 decode(source, key)
该方法将字符串source以key作为密钥进行解密，返回解密密后的字符串，密钥最长为16位
***
### views.py
前后端通信与数据处理部分，my_tools.py的方法在此调用
***
### urls.py
路由分发


