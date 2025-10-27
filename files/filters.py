from dj_rql.filter_cls import AutoRQLFilterClass
from .models import File

class FileFilterClass(AutoRQLFilterClass):
    MODEL = File