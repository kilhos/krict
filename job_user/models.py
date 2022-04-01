from django.db import models
from django.conf import settings
from django.db.models import JSONField
from django.urls import reverse

class Module(models.Model):
    module_type_list = (
        ('type1', 'type1'),
        ('type2', 'type2'),
    )

    module_category_list = (
        ('category1', 'category1'),
        ('category2', 'category2'),
    )
    level_list = (
        ('1', 'level1'),
        ('2', 'level2'),
        ('3', 'level3'),
    )
    module_name = models.CharField(max_length=100)
    module_type = models.CharField(choices=module_type_list, max_length=100)
    module_img = models.ImageField(blank=True, upload_to='job_user/module')
    module_level = models.CharField(choices=level_list, max_length=100, default='1')
    module_explanation = models.TextField()
    module_category = models.CharField(choices=module_category_list, max_length=100)
    paper_link = models.URLField()
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'module'

    def __str__(self):
        return self.module_name

    def get_absolute_url(self):
        return reverse('job_manager:module_detail', args=[self.pk])

    def get_user_login_absolute_url(self):
        return reverse('job_user:module_detail', args=[self.pk])


class Category(models.Model):
    module = models.ManyToManyField(Module)
    category_name = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'category'


class ModuleApi(models.Model):
    module = models.ForeignKey(Module, models.CASCADE)
    #module_api_name = models.FileField(blank=True, upload_to='job_user/module_api/')
    module_api_name = models.CharField(max_length=100)
    module_api_cd = models.CharField(max_length=10, default="CD001")

    def get_absolute_url(self):
        return reverse('job_manager:module_api_modify', args=[self.pk])

    class Meta:
        managed = True
        db_table = 'moduleapi'


class Job(models.Model):
    status_list = (
        ('waiting', 'waiting'),
        ('running', 'running'),
        ('complete', 'complete'),
        ('fail', 'fail'),
        ('stop', 'stop'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    module_api = models.ForeignKey(ModuleApi, on_delete=models.CASCADE)
    job_name = models.CharField(max_length=100)
    job_status = models.CharField(choices=status_list, max_length=100, default='waiting')
    smiles = models.TextField()
    job_explanation = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'job'

    def __str__(self):
        return self.job_name + '  pk(' + str(self.pk) + ')'

    def get_absolute_url(self):
        return reverse('job_user:job_detail_page', args=[self.pk])

    def get_result_url(self):
        return reverse('job_user:job_result_page', args=[self.pk])

    def get_job_result(self):
        return JobResult.objects.get(job_id=self.pk)


class JobModule(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    module_api = models.ForeignKey(ModuleApi, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'jobModule'

    def __str__(self):
        return str(self.pk)


class JobResult(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    module_api = models.ForeignKey(JobModule, on_delete=models.CASCADE)
    result_json = JSONField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'jobResult'

    def __str__(self):
        return 'result_pk : ' + str(self.pk)



