from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .forms import LoginForm
from django.views.decorators.csrf import csrf_exempt

app_name = 'accounts'


urlpatterns = [
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('id_check/', csrf_exempt(views.id_check), name='id_check'),
    
    # id 찾기
    path('recovery/id/', views.recoveryId, name='recovery_id'),
    path('recovery/id/find/', csrf_exempt(views.ajax_find_id_view), name='ajax_id'),

    # 비밀번호 찾기
    path('recovery/pw/', views.recoveryPw, name='recovery_pw'),
    path('send_mail/', csrf_exempt(views.send_mail), name='send_mail'),
    path('comfirm_auth/', csrf_exempt(views.comfirm_auth), name='comfirm_auth'),
    path('password_change/', csrf_exempt(views.password_change), name='password_change'),
]

