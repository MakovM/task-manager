from django.urls import path

from tasks.views import (
    TaskListView,
    TaskDetailView
)

app_name = "tasks"

urlpatterns = [
    path("", TaskListView.as_view(), name="task-list"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task-detail")
]
