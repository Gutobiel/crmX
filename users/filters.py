from dj_rql.filter_cls import AutoRQLFilterClass
from .models import Profile

class UserFilterClass(AutoRQLFilterClass):
    MODEL = Profile

