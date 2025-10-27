from dj_rql.filter_cls import AutoRQLFilterClass
from .models import Board

class BoardFilterClass(AutoRQLFilterClass):
    MODEL = Board