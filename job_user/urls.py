from django.urls import path

from job_user import views

app_name = 'job_user'

urlpatterns = [



    # 작업 목록 관련
    path('list/', views.job_list_page, name='job_list_page'),
    path('ajax/delete/', views.delete_job, name='delete_job'),

    # 작업 등록 화면 관련
    path('register/', views.job_register_page, name='job_register_page'),
    path('ajax/register/', views.register_job, name="register_job"),

    # 작업 디테일 관련
    path('<int:job_id>/detail/', views.job_detail, name='job_detail'),
    path('job_detail_page/<int:pk>/module_id', views.job_detail_page_api, name='job_detail_page_api'),

    path('module_search/', views.module_search, name='module_search'),
    path('module_detail/<int:pk>/', views.module_detail, name='module_detail'),
    path('module_list/', views.module_list, name='module_list'),
    path('smiles_input/', views.smiles_input, name='smiles_input'),
    path('job_result_page/', views.job_result_page_list, name='job_result_page_list'),
    path('job_result_page/<int:pk>/', views.job_result_page, name='job_result_page'),
    path('smiles_result/', views.smiles_result, name="smiles_result"),
    path('profile_modify/', views.profile_modify, name="profile_modify"),

    path('job_result_page/job_result_report/<int:pk>/', views.job_result_report, name='job_result_report'),

    path('job_status_running_change_to_completed/', views.job_status_running_change_to_completed, name='job_status_running_change_to_completed'),
    path('profile_delete/', views.profile_delete, name='profile_delete'),
    path('job_result_report_csv/<int:pk>', views.job_result_report_csv, name='job_result_report_csv'),


    path('user_password_change/', views.user_password_change, name='user_password_change')
]
