


from api.rest import *
from api.decorators import *
from myapp.models import *
from api.utils import *


#questionnaire = Questionnaire.objects.filter(id__in=ids,cusomer=request.user.custormer)
# 问题操作
class CustomerQuestion(Rest):
    @customer_required
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

    @customer_required
    def post(self, request, *args, **kwargs):
        # 更新问题
        # 找到问题
        data = request.POST
        # 问题表不具有用户和状态信息，需要通过主表查询从表的方式回去判断条件
        question = Question.objects.filter(id=data.get('id'), Questionnaire__user=request.user.custormer, Questionnaire__state__in=[0,2,3])
        if question:
            question = question[0]
        else:
            return params_error({
                "msg":"此问题不存在"
            })
        question.title = data.get('title', '提纲')
        question.category = data.get('category', 'radio')
        question.index = int(data.get('index', 0))
        question.save()
        # 更新问题所在问卷的状态
        questionnaire = question.questionnaire
        questionnaire.state = 0
        questionnaire.save()

        items = data.get('items', [])
        question.questionitem_set.all().delete()
        for item in items:
            question_item = QuestionItem()
            question_item.question = question
            question_item.content = item
            question_item.save()
        return json_response({
            "msg":"更新成功"
        })



    @customer_required
    def put(self, request, *args, **kwargs):
        # 创建问题
        # 获取前端传入的数据
        data = request.PUT
        # 找到问卷
        ids = [0, 2, 3]
        questionnaire = Questionnaire.objects.filter(id=data.get('questionnaire_id'), cusomer=request.user.custormer, state__in=ids)
        if questionnaire:
            questionnaire = questionnaire[0]
        else:
            return params_error({
                'msg':'找不到问卷，问卷不存在'
            })

        # 创建问题对象, 并添加问题
        quest = Question()
        quest.title = data.get('title')
        quest.questionnaire = questionnaire
        # 修改问卷状态
        questionnaire.state = 0
        quest.save()

        # 添加问题选项
        items = data.get('items', [])
        for item in items:
            question_item = QuestionItem()
            question_item.question = quest
            question_item.content = item
            question_item.save()
        return json_response({
            "id": quest.id
        })

    @customer_required
    def delete(self, request, *args, **kwargs):
        # 删除问题
        # 获取传入数据
        data = request.DELETE
        # 找到问题
        question = Question.objects.filter(id=data.get('id'), Questionnaire__user=request.user.custormer, Questionnaire__state__in=[0,2,3])
        if question:
            question = question[0]
        else:
            return params_error({
                "msg":"此问题不存在"
            })
        question.delete()