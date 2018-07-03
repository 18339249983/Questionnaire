import random
import json

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import url
from django.contrib.auth.models import User

from api.utils import *
from myapp.models import *

class Rest(object):
    def __init__(self, name=None):
        self.name = name or self.__class__.__name__.lower()
    # 定义一个方法，用于绑定到url中
    @csrf_exempt
    def enter(self, request, *args, **kwargs):
        # 取出客户端请求方法
        method = request.method
        # 根据请求方法执行相应的处理函数
        if method == 'GET':
            # 获取资源
            return self.get(request, *args, **kwargs)
        elif method == 'POST':
            # 更新资源
            return self.post(request, *args, **kwargs)
        elif method == 'PUT':
            # 添加资源
            return self.put(request, *args, **kwargs)
        elif method == 'DELETE':
            # 删除资源
            return self.delete(request, *args, **kwargs)
        else:
            # 不支持其他资源
            return method_not_allowed()

    def get(self, request, *args, **kwargs):
        return method_not_allowed()
    def post(self, request, *args, **kwargs):
        return method_not_allowed()
    def put(self, request, *args, **kwargs):
        return method_not_allowed()
    def delete(self,request,*args,**kwargs):
        return method_not_allowed()



class Register(object):
    def __init__(self,):
        self.resources=[]
    def regist(self, resource):
        self.resources.append(resource)

    @property
    def urls(self):
        urlpatterns = [
            url(r'^{name}$'.format(name=resource.name), resource.enter)
            for resource in self.resources
        ]
        return urlpatterns


class SessionRest(Rest):
    def put(self,request,*args,**kwargs):
        return json_response({'msg':'session put'})
    def delete(self,request,*args,**kwargs):
        return json_response({'msg':'session delete'})

class UserRest(Rest):
    def get(self, request, *args, **kwargs):
        return json_response({'msg':'user get'})
    def post(self, request, *args, **kwargs):
        print('post数据是')
        print(request.POST)
        print('http 请求体')
        data = json.loads(request.body.decode())
        print(data)
        return json_response({'msg':'user post'})
    def put(self, request, *args, **kwargs):
        data = request.PUT
        username = data.get('username','')
        password = data.get('password','')
        ensure_password = data.get('ensure_password','')
        regist_code = data.get('regist_code',0)
        session_regist_code=request.session.get('regist_code',1)
        error = dict()

        if not username:
            error['username'] = '必须提供用户名'
        else:
            if User.objects.filter(username=username).count()>0:
                error['username']='用户名已存在'
        if len(password)<6:
            error['password']='密码长度不可小于6位'
        if password != ensure_password:
            error['ensure_password']='密码不匹配'
        if regist_code != session_regist_code:
            error['regist_code']='验证码不匹配'
        if error:
            return params_error(error)
        user=User()
        user.username=username
        user.set_password(password)
        user.save()

        category = data.get('category','userinfo')

        if category=='userinfo':
            # 创建普通用户
            user_obj = UserInfo()
            user_obj.name = ""
            user_obj.qq = ""
        else:
            # 创建客户
            user_obj = Custormer()
            user_obj.name=""
            user_obj.email=""

        user_obj.user=user
        user_obj.save()
        print('成功')
        return json_response({'id':user.id})

class RegistCode(Rest):
    def get(self, request, *args, **kwargs):
        # 获取随机验证码
        regist_code = random.randint(100000,1000000)
        # 保存到session中
        request.session['regist_code'] = regist_code
        # 返回随机数
        return json_response({
            'regist_code':regist_code
        })