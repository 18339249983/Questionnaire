from api.utils import *


# 登陆用户必须为客户，只能在类中使用
def customer_required(func):
    def _wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return not_authenbticated()
        user = request.user
        if not hasattr(user, 'custormer'):
            return permission_denied()
        return func(self,request, *args, **kwargs)
    return _wrapper


# 登录用户必须为普通用户，只能在类中使用
def userinfo_required(func):
    def _wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return not_authenbticated()
        user = request.user
        if not hasattr(user, 'userinfo'):
            return permission_denied()
        return func(self, request, *args, **kwargs)
    return _wrapper


# 登录用户必须为超级用户,只能在类中使用
def superuser_required(func):
    def _wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return not_authenbticated()
        return func(self, request, *args, **kwargs)
    return _wrapper