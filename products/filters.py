from dj_rql.filter_cls import AutoRQLFilterClass
from .models import Product

class ProductFilterClass(AutoRQLFilterClass):
    MODEL = Product