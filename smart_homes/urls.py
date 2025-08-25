from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include, re_path
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

]
