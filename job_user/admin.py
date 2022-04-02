from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Module,Job, JobResult, ModuleApi


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['id', 'module_img_tag', 'module_name', 'module_type']
    list_display_links = ['id', 'module_img_tag', 'module_name', 'module_type']
    search_fields = ['module_name']

    def module_img_tag(self, module):
        if module.module_img:
            return mark_safe(f'<img src=" {module.module_img.url}" style="width:72px;"/>')
        return None

@admin.register(ModuleApi)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['id', 'module_api_name']
    list_display_links = ['id', 'module_api_name']
    search_fields = ['module_api_name']


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'job_name', 'job_status']
    list_display_links = ['id', 'user']
    search_fields = ['user']


@admin.register(JobResult)
class JobResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'job']
    list_display_links = ['id', 'job']
    search_fields = ['job']

