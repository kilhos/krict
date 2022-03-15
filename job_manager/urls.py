from django.urls import path, include
from . import views

app_name = 'job_manager'

urlpatterns = [
    path('member_manager/', views.member_manager, name='member_manager'),
    path('member_manager/modify/<int:pk>/', views.member_modify, name='member_modify'),
    path('member_manager/modify_save/<int:pk>/', views.member_modify_save, name='member_modify_save'),
    path('module_manager/', views.module_manager, name='module_manager'),
    path('module_register/', views.module_register, name='module_register'),
    path('module_search/', views.module_search, name='module_search'),
    path('module_detail/<int:pk>/', views.module_detail, name='module_detail'),
    path('module_detail_save/<int:pk>/', views.module_detail_save, name='module_detail_save'),
    path('module_modify/<int:pk>/', views.module_modify, name='module_modify'),
    path('do_module_modify', views.do_module_modify, name='do_module_modify'),
    path('module_delete/', views.module_delete, name='module_delete'),
    path('module_api_manage/', views.module_api_manage, name='module_api_manage'),
    path('module_api_modify/<int:pk>/', views.module_api_modify, name='module_api_modify'),
    path('module_api_modify_save/<int:pk>/', views.module_api_modify_save, name='module_api_modify_save'),

    path('test/', views.test, name='test'),
]
