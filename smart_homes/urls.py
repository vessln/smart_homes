from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include, re_path
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),

    path("", include("smart_homes.common.urls")),
    path("account/", include("smart_homes.account.urls")),
    # path("shop/", include("smart_homes.products.urls")),
    # path("order/", include("smart_homes.order.urls")),
]