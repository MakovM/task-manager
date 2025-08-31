from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("tasks.urls", namespace="tasks")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
] + debug_toolbar_urls()
