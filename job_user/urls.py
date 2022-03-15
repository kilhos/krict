from django.urls import path

from job_user import views

app_name = 'job_user'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('job_list/', views.job_list, name='job_list'),
    path('job_detail_page/<int:pk>/', views.job_detail_page, name='job_detail_page'),
    path('job_detail_page/<int:pk>/module_id', views.job_detail_page_api, name='job_detail_page_api'),
    path('job_register_page/', views.job_register_page, name='job_register_page'),
    path('job_register_page/module_id', views.job_register_page_api, name='job_register_page_api'),
    path('job_register/', views.job_register, name='job_register'),
    path('module_search/', views.module_search, name='module_search'),
    path('module_detail/<int:pk>/', views.module_detail, name='module_detail'),
    path('module_list/', views.module_list, name='module_list'),
    path('smiles_input/', views.smiles_input, name='smiles_input'),
    path('job_result_page/', views.job_result_page_list, name='job_result_page_list'),
    path('job_result_page/<int:pk>/', views.job_result_page, name='job_result_page'),
    path('smiles_result/', views.smiles_result, name="smiles_result"),
    path('profile/', views.profile, name="profile"),
    path('profile_modify/', views.profile_modify, name="profile_modify"),
    path('job_regist/insert/', views.job_insert, name="insert"),
    path('job_detail_page/<int:pk>/modify', views.job_detail_page_modify, name='job_detail_page_modify'),
    path('job_detail_page/<int:pk>/delete', views.job_detail_page_delete, name='job_detail_page_delete'),
    path('job_result_page/job_result_report/<int:pk>/', views.job_result_report, name='job_result_report'),
    path('siteMap/', views.siteMap, name='siteMap'),
    path('contactUs/', views.contactUs, name='contactUs'),
    path('privacyPolicy/', views.privacyPolicy, name='privacyPolicy'),
    path('job_status_running_change_to_completed/', views.job_status_running_change_to_completed, name='job_status_running_change_to_completed'),
    path('profile_delete/', views.profile_delete, name='profile_delete'),
    path('job_result_report_csv/<int:pk>', views.job_result_report_csv, name='job_result_report_csv'),
    path('job_delete/', views.job_delete, name='job_delete'),

    path('user_password_change/', views.user_password_change, name='user_password_change')
]
