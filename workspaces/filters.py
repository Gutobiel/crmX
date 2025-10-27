from dj_rql.filter_cls import AutoRQLFilterClass
from .models import Workspace

class WorkspaceFilterClass(AutoRQLFilterClass):
    MODEL = Workspace