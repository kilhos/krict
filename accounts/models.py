from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    state_list = (
        ('non','승인전'),
        ('liv','승인'),
        ('del','탈퇴'),
    )
    role_list = (
        ('sup','관리자'),
        ('gen','일반사용자'),
    )
    level_list = (
        ('1','level1'),
        ('2','level2'),
        ('3','level3'),
    )

    name = models.CharField(max_length=100, default="")
    institution = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(choices=state_list, default='non', max_length=100)
    role = models.CharField(choices=role_list, default='gen', max_length=100)
    level = models.CharField(choices=level_list, default='1', max_length=100)
    department = models.CharField(max_length=100, null=True, blank=True)
    employee_no = models.CharField(max_length=100, null=True, blank=True)
    mobile_phone = models.CharField(max_length=100, null=True, blank=True)
    company_phone = models.CharField(max_length=100, null=True, blank=True)
    modify_date = models.DateTimeField(auto_now=True)
    auth = models.CharField(max_length=4, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('job_manager:member_modify', args=[self.pk])