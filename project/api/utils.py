
import json

from django.http.response import HttpResponse

def method_not_allowed():
    return HttpResponse('{"msg":"方法不支持"}', status=405, content_type='application/json')

def params_error(error):
    return HttpResponse(json.dumps(error), status=422, content_type='application/json')

def not_authenbticated():
    return HttpResponse('{"msg":"未登录"}', status=401, content_type='application/json')


def permission_denied():
    return HttpResponse('{"msg":"没有权限"}', status=403, content_type='application/json')


def json_response(data):
    return HttpResponse(json.dumps(data), status=200, content_type='application/json')