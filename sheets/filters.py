from dj_rql.filter_cls import AutoRQLFilterClass
from .models import Sheet

class SheetFilterClass(AutoRQLFilterClass):
    MODEL = Sheet