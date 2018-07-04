from django.db import models
from datetime import date
from django.contrib.auth.models import User
# Create your models here.


# 客户信息
class Custormer(models.Model):
    user = models.OneToOneField(User)
    username = models.CharField(default='名称',max_length=20, help_text='客户名称')
    email = models.CharField(default='', max_length=30, null=True, blank=True, help_text='邮箱')
    company = models.CharField(default='', max_length=40, null=True, help_text='公司名称')
    address = models.CharField(default='', max_length=50, null=True, help_text='地址')
    phone = models.CharField(default='', max_length=16,blank=True,null=True,help_text='手机号')
    mobile = models.CharField(default='',max_length=20,blank=True,null=True,help_text='固定电话')
    qq = models.CharField(default='',max_length=20,blank=True,null=True,help_text='qq')
    wechat = models.CharField(default='',max_length=20,blank=True,null=True,help_text='微信号')
    web = models.CharField(default='', max_length=50,blank=True,null=True,help_text='网站')
    industry = models.CharField(default='',max_length=50,blank=True,null=True,help_text='行业')
    description = models.TextField(default='', null=True,blank=True,help_text='公司简介')

    @classmethod
    def create(cls, user, **kwargs):
        return cls(username=user,**kwargs)

# 用户信息表
class UserInfo(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(default='姓名',max_length=15,null=True,blank=True,help_text='姓名')
    age = models.IntegerField(default=1, help_text='年龄')
    gender = models.BooleanField(default=1,max_length=18, help_text='性别')
    phone = models.CharField(default='', max_length=16,blank=True, null=True, help_text="手机号码")
    email = models.EmailField(default='',blank=True,null=True,help_text='邮箱')
    address = models.CharField(default='', max_length=256, blank=True, null=True, help_text="地址")
    birthday = models.DateField(default=date(2018, 1, 1), null=True, help_text="出生日期")
    qq = models.CharField(default='', max_length=16, blank=True, null=True, help_text='qq')
    wechat = models.CharField(default='', max_length=16, blank=True, null=True, help_text='微信')
    job = models.CharField(default='', max_length=64, blank=True, null=True, help_text='工作')
    salary = models.CharField(default='', max_length=32, blank=True, null=True, help_text='薪水')


# 问卷
class Questionnaire(models.Model):
    cusomer =  models.ForeignKey('Custormer', help_text='客户信息')
    title = models.CharField(default='标题', max_length=64, help_text='标题')
    create_date = models.DateTimeField(help_text='创建时间')
    deadline = models.DateTimeField(help_text='截止时间')
    state = models.IntegerField(default=0, help_text="""状态,0-->草稿,1-->待审核,2-->审核失败,3-->审核成功,4-->发布成功""")
    quantity = models.IntegerField(default=1, help_text='发布数量')
    free_count = models.IntegerField(default=1, help_text='可用问卷数量')


# 题目
class Question(models.Model):
    category_choice = [
        ('radio', '单选'),
        ('select', '多选'),
    ]
    questionnaire = models.ForeignKey('Questionnaire', help_text='关联问卷', on_delete=models.CASCADE)
    title = models.CharField(max_length=128, help_text='题目')
    index = models.IntegerField(default=0, help_text='题目题号')
    category = models.CharField(choices=category_choice, default='redio', max_length=16, help_text='是否多选')
    type = models.BooleanField(default=1, help_text='1->必答题， 0->非必答')


# 题目选项
class QuestionItem(models.Model):
    question = models.ForeignKey('Question', help_text='关联题目', on_delete=models.CASCADE)
    content = models.CharField(max_length=32, help_text='选项内容')


# 客户钱包
class Wallet(models.Model):
    customer = models.OneToOneField('Custormer', help_text='客户')
    balance = models.IntegerField(default=0, help_text='余额')


# 充值记录
class Recharge(models.Model):
    wallet = models.ForeignKey('Wallet',help_text='关联钱包')
    create_date = models.DateTimeField(auto_now=True, help_text='充值时间')
    money = models.FloatField(default='', help_text='充值金额')
    station = models.BooleanField(default=False, help_text='完成支付为True, 未完成为Flase')
    payment = models.CharField(max_length=32, choices=[('alipay','支付宝'),('wechat','微信')], help_text='支付方式')
    paymentid = models.CharField(max_length=128, help_text='第三方支付id')


# 交易记录
class DealRecord(models.Model):
    wallet = models.ForeignKey('Wallet', help_text='关联钱包')
    create_date = models.DateTimeField(auto_now=True, help_text='消费时间')
    money = models.FloatField(default='', help_text='充值金额')
    station = models.BooleanField(default=False, help_text='完成支付为True, 未完成为Flase')
    paymentid = models.CharField(max_length=128, help_text='第三方支付id')

# 管理员
class Administrator(models.Model):
    user = models.OneToOneField(User)
    username = models.CharField(default='姓名', max_length=20, help_text='姓名')
    password = models.CharField(default='',max_length=20, help_text='密码')


# 问卷审核
class QuestionnaireComment(models.Model):
    questionnaire = models.ForeignKey('Questionnaire', help_text='问卷', on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True, help_text='审核时间')
    comment = models.TextField(help_text='审核批注')


# 积分
class Point(models.Model):
    userinfo = models.OneToOneField('UserInfo', help_text='用户信息')
    balance = models.IntegerField(default=0, help_text='余额')

# 积分获取记录
class GetPoint(models.Model):
    point = models.ForeignKey('Point',help_text='关联积分')
    get_date = models.DateTimeField(auto_now=True, help_text='获取时间')
    reasion = models.CharField(default='', max_length=50, help_text='获取原因')
    amount = models.IntegerField(help_text='积分总数')


# 积分使用记录
class PutPoint(models.Model):
    point = models.ForeignKey('Point', help_text='关联积分')
    get_date = models.DateTimeField(auto_now=True, help_text='消费时间')
    reasion = models.CharField(default='', max_length=50, help_text='消费原因')
    amount = models.IntegerField(help_text='积分总数')


# 参与问卷
class JoinQuestion(models.Model):
    userinfo = models.ForeignKey('UserInfo', null=True, help_text='关联用户')
    questionnaire = models.ForeignKey('Questionnaire',help_text='关联问卷')
    create_date = models.DateTimeField(auto_now=True, help_text='创建时间')
    is_done = models.BooleanField(default=False, help_text='是否已经完成')

# 用户选项
class Iterm(models.Model):
    userinfo = models.ForeignKey('UserInfo', help_text='关联用户')
    questionItem = models.ForeignKey('QuestionItem', help_text='关联选项')

