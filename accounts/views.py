import hashlib
from random import randint
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic import TemplateView, View
from .forms import SignupForm, CustomAuthenticationForm
from django.contrib.auth.views import (LoginView, logout_then_login, PasswordChangeView as AuthPasswordChangeView)
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from accounts.decorators import *
from django.utils.decorators import method_decorator
from .forms import RecoveryIdForm, RecoveryPwForm, PasswordChangeForm
from django.core.mail import send_mail, EmailMessage
from django.urls import reverse_lazy
from django.contrib.auth import login as auth_login


User = get_user_model()


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'


profile = ProfileView.as_view()


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            #auth_login(request, signed_user) 회원가입 후 바로로그인
            messages.success(request, '회원가입 환영합니다.')
            return redirect("/")
        else:
            messages.error(request, 'Validation Error!.')
    else:
        form = SignupForm()
    return render(request,'accounts/signup_form.html', {
        'form':form,
    })


class AuthLoginView(LoginView):

    template_name = "accounts/login.html"
    form_class = CustomAuthenticationForm


login = logout_message_required(AuthLoginView.as_view())


@login_required()
def logout(request):
    messages.success(request, "로그아웃되었습니다.")
    return logout_then_login(request)


@logout_message_required
def id_check(request):
    val_check = False
    if request.method == 'POST':
        get_id = request.POST['user_id']
        if User.objects.filter(username=get_id):
            val_check = True

    return HttpResponse(json.dumps(val_check), content_type="text/json-commnet-filtered")


class RecoveryIdView(View):
    template_name = 'accounts/recovery_id.html'
    recovery_id = RecoveryIdForm

    def get(self, request):
        if request.method=='GET':
            form = self.recovery_id(None)
        return render(request, self.template_name, { 'form': form, })


recoveryId = logout_message_required(RecoveryIdView.as_view())


@logout_message_required
def ajax_find_id_view(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    result_id = User.objects.get(name=name, email=email)

    return HttpResponse(json.dumps({"result_id": result_id.username}, cls=DjangoJSONEncoder),
                        content_type="application/json")


class RecoveryPwView(View):
    template_name = 'accounts/recovery_pw.html'
    recovery_pw = RecoveryPwForm

    def get(self, request):
        if request.method=='GET':
            form = self.recovery_pw(None)
        return render(request, self.template_name, { 'form': form, })


recoveryPw = logout_message_required(RecoveryPwView.as_view())


@logout_message_required
def send_mail(request):
    """
    username = request.POST['username']
    name = request.POST['name']
    email = request.POST['email']
    auth_num = randint(1000,9999)
    target_user = User.objects.get(username=username, name=name)
    target_user.auth = auth_num
    target_user.save()
    save_target_user = User.objects.get(username=username, name=name, auth=auth_num)
    try:
        content = {'auth_num': auth_num}
        msg_html = render_to_string('accounts/email_format.html', content)
        msg = EmailMessage(subject="인증 코드 발송 메일", body=msg_html, from_email='pranpreten89@gmail.com', bcc=[email])
        msg.content_subtype='html'
        msg.send()
        return HttpResponse(json.dumps({'save_target_user':save_target_user.pk}), content_type="text/json-commnet-filtered")
    except:
        return HttpResponse("email send fail")
    """
    username = request.POST['username']
    name = request.POST['name']
    email = request.POST['email']
    target_user = User.objects.get(username=username, name=name, email=email)        
    if target_user:
        return HttpResponse(json.dumps({'save_target_user':target_user.pk}), content_type="text/json-commnet-filtered")
    else:
        return HttpResponse(json.dumps({'save_target_user':'false'}), content_type="text/json-commnet-filtered")

@logout_message_required
def comfirm_auth(request):
    user_pk = request.POST['user_pk']
    auth_num = request.POST['auth_num']
    target_user = User.objects.get(pk=user_pk)
    if auth_num == target_user.auth:
        return HttpResponse(json.dumps({'target_user':target_user.pk}), content_type="text/json-commnet-filtered")
    else:
        return HttpResponse(json.dumps({'target_user': 'false'}), content_type="text/json-commnet-filtered")


@logout_message_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        pk = request.POST['pk']
        target_user = User.objects.get(pk=pk)
        if form.is_valid():
            target_user.password = request.POST['password1']
            target_user.set_password(request.POST['password1'])
            target_user.save()
            return redirect("accounts:login")
    else:
        form = PasswordChangeForm

    return render(request, 'accounts/password_change.html', {'form': form, 'pk': request.GET['pk']})



