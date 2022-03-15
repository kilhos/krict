from accounts.models import *
from job_user.models import *
from job_manager.models import *


def user_context(request):
    return {'users':User.objects.all()}


def module_list(request):
    modules = Module.objects.all()
    for mod in modules:
        cut_idx = mod.module_explanation.find("//")
        changed_mod_ex = mod.module_explanation[:cut_idx]
        mod.module_explanation = changed_mod_ex
    return {'modules':modules}