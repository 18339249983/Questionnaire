from datetime import datetime, timedelta

from api.utils import *
from api.decorators import *
from myapp.models import *
from api.rest import *

class AdminQuersionnaire(Rest):
    @superuser_required
    def get(self, request, *args, **kwargs):
        # 获取问卷
        data = request.GET
        user = request.user.custormer
        # 创建空字典接受所需信息
        datas = dict()
        page = data.get('page', 1)
        limit = data.get('limit', 10)
        status = data.get('status', 0)
        with_detail = data.get('with_detail', False)
        questionnaire = Questionnaire.objects.all()[(page - 1) * limit: page * limit]
        id = data.get('id', '')
        # 是否获取单个问卷
        if id == '':
            datas['pages'] = page
            datas['count'] = limit
            datas['objs'] = []
            # questionnaire[(page - 1) * limit: page * limit]
            detil = dict()
            for i in questionnaire:
                detil['id'] = i.id
                detil['title'] = i.title
                detil['quantity'] = i.quantity
                detil['free_quantity'] = i.free_count
                # 时间转换字符串用strftime
                detil['expire_date'] = datetime.strftime(i.deadline, "%Y-%m-%d")
                detil['create_date'] = datetime.strftime(i.create_date, "%Y-%m-%d")
                detil['status'] = i.state
                detil['customer'] = [{
                    "id": user.id,
                    "name": ""
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

class QuestionnaireComment(Rest):
    @superuser_required
    def put(self, request, *args, **kwargs):
        data = request.PUT
        questionnaire = Questionnaire.objects.filter(id=data.get('questionnaire_id'), state=1)
        if questionnaire:
            questionnaire = questionnaire[0]
        else:
            return params_error({
                "questionnaire_id":"该问卷找不到"
            })
        is_agree = data.get('is_agree')
        if is_agree:
            questionnaire.state = 3
            questionnaire.save()
            return json_response({
                "comment":"审核通过"
            })
        comment = data.get('comment','')
        if comment:
            questionnaire.state = 2
            questionnaire.save()
            questionnaire_comment = QuestionnaireComment()
            questionnaire_comment.datetime = datetime.now()
            questionnaire_comment.comment = comment
            questionnaire_comment.questionnaire = questionnaire
            questionnaire_comment.save()
            return json_response({
                "comment": "提交审核内容成功"
            })
        return params_error({
            "comment":"没有提供审核信息"
        })



