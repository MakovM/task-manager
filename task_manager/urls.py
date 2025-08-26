from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("task/", include("tasks.urls", namespace="tasks")),
    path("", include("accounts.urls", namespace="accounts")),
] + debug_toolbar_urls()
