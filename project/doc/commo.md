# 通用接口
## 获取验证码

method: GET

api:'/api/v1/registcode'

body: None

response:

'''json
{
    "regist_code":345693//返回的验证码
}
'''

## 用户接口
### 注册用户

method:PUT

api:'/api/v1/user'

body:
- **username**:用户名
- **password**:密码
- **ensure_password**:确认密码
- **regist_code**:注册码

response:

'''json
{
    "id":1//新建的用户id
}
'''

### 获取用户信息

method: GET

api: '/api/v1/user'

body: None

response:

'''json
{
    "name":"千峰",//名称
    "email":"",//邮箱
    "user":"",//用户id
    "category":"customer",//用户类型
}
'''

// 或者
{
    "name":"",//姓名
    "qq":"",//qq号
    "user":2,//用户id
    "category":"userinfo"//用户类型
}

### 更新用户信息

method:POST

api: '/api/v1/user'

body:
- name:姓名
- emal:邮箱
- qq:qq号

response:
'''json
{
    "msg":"更新成功"
}
'''

## 会话

## 登陆

method:PUT

api: '/api/v1/session'

body:
- **username**: 用户名
- *password**: 密码

response:
'''json
{
    "msg":"登陆成功"
}
'''

### 登陆

method:DELETE

api: '/api/v1/session'

body:None

respone:
'''json
{
    "msg":"退出成功"
}
'''

