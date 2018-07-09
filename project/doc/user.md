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


