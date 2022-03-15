from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
#from django_pydenticon.views import image as pydenticon_image


urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('manager/', include('job_manager.urls')),
    path('', include('job_user.urls')),
    path('admin/', admin.site.urls),
    #path('identicon/image/<path:data>/', pydenticon_image,name='pydenticon_image'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)