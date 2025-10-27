from dj_rql.filter_cls import AutoRQLFilterClass
from .models import Element

class ElementFilterClass(AutoRQLFilterClass):
    MODEL = Element

