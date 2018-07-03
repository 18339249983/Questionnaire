# 系统包
import os
import sys

# 第三方扩展包
from django.conf.urls import url

# 自定义包
from api.rest import *

# # 新建一个session对象
# session_obj=SessionRest()
# # 新建user对象
# user_obj = UserRest()
#
# api_urls = [
#     url(r'session', session_obj.enter),
#     url(r'user', user_obj.enter)
# ]

api=Register()
api.regist(SessionRest('session'))
api.regist(UserRest('user'))
api.regist(RegistCode())