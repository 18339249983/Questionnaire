import random
import json

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import url
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login


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
        data = request.PUT
        username = data.get('username', '')
        password = data.get('password', '')
        # 查询数据库用户表
        user = authenticate(username=username,password=password)
        if user:
            # 保存登陆状态
            login(request,user)
            return json_response({
                "msg":"登陆成功"
            })
        else:
            return params_error({
                "msg":"用户或密码错误"
            })
    def delete(self,request,*args,**kwargs):
        logout(request)

        return json_response({'msg':'退出成功'})

class UserRest(Rest):
    def get(self, request, *args, **kwargs):
        user=request.user
        if user.is_authenticated:
            # 获取信息
            data=dict()
            if hasattr(user,'custormer'):
                custome=user.custormer
                data['username']=custome.username
                data['email']=custome.email
                data['user']=user.id
                data['category']='customer'
            elif hasattr(user,'userinfo'):
                userinfo=user.userinfo
                data['username'] = userinfo.username
                data['qq'] = userinfo.qq
                data['user'] = user.id
                data['category'] ='userinfo'
            else:
                return json_response({})
        else:
            return not_authenbticated()
        return json_response(data)

    def post(self, request, *args, **kwargs):
        # 判断用户是否登陆
        data = request.POST
        user = request.user
        if request.user.is_authenticated:
            # 是否具有某个属性
            if hasattr(request.user, 'customer'):
                # data = request.POST
                customer = user.customer
                customer.username = data.get('username', '')
                customer.email = data.get('email', '')
                customer.save()
            elif hasattr(request.user, 'userinfo'):
                # data = request.POST
                userinfo = user.userinfo
                userinfo.username = data.get('username', '')
                userinfo.qq = data.get('qq', '')
                userinfo.save()
            else:
                return json_response({
                    "msg":"更新成功~~~"
                })
        else:
            return not_authenbticated()
        return json_response({
            "msg":"更新成功"
        })
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

        category = data.get('category', 'userinfo')
        if category == 'customer':
            # 创建客户
            user_obj = Custormer()
            user_obj.username = username
            user_obj.email = ""
            user_obj.company = ""
            user_obj.address = ""
            user_obj.phone = ""
            user_obj.mobile = ""
            user_obj.qq = ""
            user_obj.wechat = ""
            user_obj.web = ""
            user_obj.industry = ""
            user_obj.description = ""

        else:
            # 创建普通用户
            user_obj = UserInfo()
            user_obj.name = username
            user_obj.qq = ""
            user_obj.age = 1
            user_obj.gender = 1
            user_obj.phone = ""
            user_obj.email = ""
            user_obj.address = ""
            user_obj.birthday = date(2018,1,1)
            user_obj.wechat = ""
            user_obj.job = ""
            user_obj.salary = ""
        user_obj.user = user
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