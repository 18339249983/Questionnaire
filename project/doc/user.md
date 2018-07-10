# 用户接口
 
## 参与信息

### 参与问卷

method: PUT

api: '/api/v1/join_questionnaire'

body:
- **questionnaire_id**: 问卷id

response:
```json
{
  "msg":"参与成功"
}
```

### 退出参与

method: DELETE

api: '/api/v1/participation'

body:

- **ids**: 参与信息id列表，例如ids:[1,2,3]

response:
```json
{
  "delete_ids":[2,3]
}
```



## 查看参与信息

method: GET

api:'/api/v1/participation

body:
- state:参与信息状态， 默认False
- page: 第几页，默认1
- limit: 每页数量，默认10

response:
```json
[
  {
    "questionnaire":{
      "title":"问卷1"
    },
    "join_date":"2018-10-10",
    "state":"is_done"
  }
]
```




## 答案

### 提交答案

method: PUT

api: '/api/v1/answer'

body:
- **item_id**:选项id

response:
```json
{
  "msg":"提交成功"
}
```


### 删除答案

method: DELETE

api: '/api/v1/answer'

body:
- **item_ids**: 选项id列表，如ids:[1,2,3]

response:
```json
{
  "delete_ids":[2,3]
}
```



## 用户产看问卷答案

method: GET

api:'/api/v1/user_answer'

body:
- **questionnaire_id**: 问卷id

response:
```json
{
  "questionnaire":{
      "title": "测试问卷",//问卷标题
      "expire_date":"2018-10-10",//问卷截止日期
      "customer":"千峰",//问卷所属客户名称
  },
  "questions":[{
    "title":"问题1",
    "category":"radio",
    "id": 1,
    "items":[
      {
        "id": 1,
        "content": "选项1",
        "is_select":false,
      }
    ]
  
  }]
}
```




## 用户完成答题

method: POST

api: '/api/v1/participation_state'

body:

- **questionnaire_id**: 问卷id

response:
```json
{
  "msg":"提交成功"
}

```



## 用户查看积分

method: GET

api:'/api/v1/user_point_history'

body:
- category: 积分类型，false代表消费，true代表获取，默认false
- page: 第几页，默认1
- limit: 每页数量，默认10

response:
```json
{
  "balance":1000, //积分数量
  "histories":[
    {
      "create_date": "2018-10-10",//历史时间
      "amount": 10, //数量
      "reason": "提交问卷"
    }
  ]
}
```


