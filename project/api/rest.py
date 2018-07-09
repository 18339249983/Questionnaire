import random
import json
from datetime import datetime

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import url
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login


from api.utils import *
from myapp.models import *
from api.decorators import *

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
            # 有坑，定义表时，表名为custormer 正确的是customer，涉及到此表的都要注意
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


# 问卷操作
class CustomerQuestionnaire(Rest):
    @customer_required
    def get(self, request, *args, **kwargs):
        # 获取问卷
        data = request.GET
        user = request.user.custormer
        # 创建空字典接受所需信息
        datas = dict()
        page = data.get('page',1)
        limit = data.get('limit',10)
        status = data.get('status',0)
        with_detail = data.get('with_detail',False)
        questionnaire = Questionnaire.objects.all()[(page - 1) * limit: page * limit]
        id = data.get('id','')
        # 是否获取单个问卷
        if id == '':
            datas['pages']=page
            datas['count']=limit
            datas['objs']=[]
            # questionnaire[(page - 1) * limit: page * limit]
            detil = dict()
            for i in questionnaire:
                detil['id']=i.id
                detil['title']=i.title
                detil['quantity']=i.quantity
                detil['free_quantity']=i.free_count
                # 时间转换字符串用strftime
                detil['expire_date']=datetime.strftime(i.deadline, "%Y-%m-%d")
                detil['create_date']=datetime.strftime(i.create_date, "%Y-%m-%d")
                detil['status']=i.state
                detil['customer']=[{
                    "id": user.id,
                    "name":""
                }]
                if with_detail in ['true', True]:
                    # 构建问卷下的问题
                    detil['questions'] = []
                    for question in i.question_set.all().order_by('index'):
                        # 构建单个问题
                        question_dic = dict()
                        question_dic['id'] = question.id
                        question_dic['title'] = question.title
                        question_dic['category'] = question.category
                        question_dic['index'] = question.index
                        # 构建问题选项
                        question_dic['item'] = [{
                            "id": item.id,
                            "content": item.content
                        } for item in question.questionitem_set.all()]
                        # 将问题添加到问卷的问题列表中
                        detil['questions'].append(question_dic)
                    detil['comments'] = [{
                        'id': item.id,
                        'create_date': datetime.strftime(item.create_date, '%Y-%m-%d'),
                        'comment': item.comment
                    } for item in i.questionnairecomment_set.all()]
                datas['objs'].append(detil)

        else:
            questionnaire = Questionnaire.objects.get(id=data.get('id'))
        return json_response(datas)


    @customer_required
    def post(self, request, *args, **kwargs):
        # 更新问卷
        data = request.POST
        # get返回对象   state__in=[0,2,3]
        questionnaire = Questionnaire.objects.filter(cusomer=request.user.custormer).get(id=data.get('id'))
        if questionnaire.state in (0,2,3):
            questionnaire.title = data.get('title', '未命名')
            questionnaire.create_date = datetime.strftime(datetime.utcnow(),'%Y-%m-%d')
            questionnaire.deadline = datetime.strptime(data.get('deadline',''),'%Y-%m-%d')
            questionnaire.quantity = data.get('quantity')
            questionnaire.free_count = data.get('quantity', 1)
            questionnaire.save()
        else:
            return json_response({"msg":"该问卷现在不能修改"})
        return json_response({"id":questionnaire.id})

    @customer_required
    def put(self, request, *args, **kwargs):
        # 创建问卷
        # 获取前端传入数据
        data = request.PUT
        # 获取当前用户的信息
        user = request.user.custormer
        # 创建问卷对象
        questionnaire = Questionnaire()
        # 值得注意， 传入的是个对象
        questionnaire.cusomer = user
        questionnaire.title = data.get('title','')
        # questionnaire.create_date = date(2018,10,10)
        questionnaire.deadline = datetime.strptime(data.get('deadline',''),'%Y-%m-%d')
        questionnaire.quantity = 100
        questionnaire.state = 0
        questionnaire.free_count = 100
        questionnaire.save()
        return json_response({"id":questionnaire.id})

    @customer_required
    def delete(self,request,*args,**kwargs):
        # 删除问卷
        data = request.DELETE
        # 获取每一个要删除的id
        if len(data.get('ids')) != 0:
            for id in data.get('ids'):
                questionnaire = Questionnaire.objects.filter(cusomer=request.user.custormer.id).get(id=id)
                questionnaire.delete()
                return json_response({"delete_ids": data.get('ids')})
        else:
            return json_response({"msg":"未选择任何问卷"})
#questionnaire = Questionnaire.objects.filter(id__in=ids,cusomer=request.user.custormer)

# 问卷状态
# 提交和发布
class Questiongnaire_state(Rest):
    # 更改问卷状态
    @customer_required
    def put(self, request, *args, **kwargs):
        data = request.PUT
        questionnaire = Questionnaire.objects.get(id=data.get('id'), user=request.user.custormer, state__in=[0,2,3])
        if questionnaire:
            questionnaire=questionnaire[0]
        else:
            params_error({
                "msg":"找不到该问卷"
            })
        questionnaire.state = data.get('state', 0)
        questionnaire.save()
        if data.get('state') == 1:
            return json_response({
                "msg":"提交审核成功"
            })
        if Questionnaire.state == 3:
            questionnaire.state = data.get('state')
            return json_response({
                "msg": "发布成功"
            })
        return params_error({
            "msg":"此状态不能发布"
        })

