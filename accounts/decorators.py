from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from .models import User
from django.http import HttpResponse


# 관리자 권한 확인
def admin_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.role != 'sup':
            messages.info(request, "접근 권한이 없습니다.")
            return redirect('job_user:main_page')
        return function(request, *args, **kwargs)

    return wrap


# 비로그인 확인
def logout_message_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "접속중인 사용자입니다.")
            return redirect('job_user:main_page')
        return function(request, *args, **kwargs)

    return wrap
