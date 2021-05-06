from django.contrib import admin
from django.urls import path, include
from transfer import views

from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('howtowork/', views.howtowork, name="howtowork"),
    path('mobiletransfer/', views.mobiletransfer, name="mobiletransfer"),
    path('about/', views.about, name="about"),
    path('api/v1/', include('authentication.urls')),

]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, ducoment_root=settings.MEDIA_ROOT)
