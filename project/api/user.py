

from api.utils import *
from api.decorators import *
from myapp.models import *
from api.rest import *

class CheckQuestionnair(Rest):
    def get(self, request, *args, **kwargs):
        # 查看所有的问卷
        pass
