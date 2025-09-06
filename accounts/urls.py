from django.urls import path, include
from accounts.views import (
    SignUpView,
    WorkerListView,
    WorkerDetailView,
    WorkerUpdateView,
    WorkerDeleteView,
    WorkerPasswordChangeView,
    WorkerPositionChangeView,
    WorkerStatusChangeView,
    PositionListView,
    PositionCreateView,
    PositionUpdateView,
    PositionDeleteView,
)

app_name = "accounts"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("signup/", SignUpView.as_view(), name="sign-up"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path(
        "workers/<int:pk>/",
        WorkerDetailView.as_view(),
        name="worker-detail"
    ),
    path(
        "workers/<int:pk>/update/",
        WorkerUpdateView.as_view(),
        name="worker-update"
    ),
    path(
        "workers/<int:pk>/delete/",
        WorkerDeleteView.as_view(),
        name="worker-delete"
    ),
    path(
        "workers/<int:pk>/password/change/",
        WorkerPasswordChangeView.as_view(),
        name="password-change",
    ),
    path(
        "workers/<int:pk>/position/change/",
        WorkerPositionChangeView.as_view(),
        name="position-change",
    ),
    path(
        "workers/<int:pk>/status/change/",
        WorkerStatusChangeView.as_view(),
        name="status-change",
    ),
    path(
        "workers/positions/",
        PositionListView.as_view(),
        name="position-list"
    ),
    path(
        "workers/positions/create/",
        PositionCreateView.as_view(),
        name="position-create"
    ),
    path(
        "workers/positions/<int:pk>/update/",
        PositionUpdateView.as_view(),
        name="position-update",
    ),
    path(
        "workers/positions/<int:pk>/delete/",
        PositionDeleteView.as_view(),
        name="position-delete",
    ),
]
