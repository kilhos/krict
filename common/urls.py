from django.urls import path

from common import views

app_name = 'common'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('siteMap/', views.siteMap, name='siteMap'),
    path('profile/', views.profile, name="profile"),
    path('contactUs/', views.contactUs, name='contactUs'),
    path('privacyPolicy/', views.privacyPolicy, name='privacyPolicy'),
]
