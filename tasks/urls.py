from django.urls import path

from tasks.views import (
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskToggleView,
    TagListView,
    TagCreateView,
    TagUpdateView,
    TagDeleteView,
)

app_name = "tasks"

urlpatterns = [
    path("", TaskListView.as_view(), name="task-list"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("task/create/", TaskCreateView.as_view(), name="task-create"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("task/<int:pk>/toggle/", TaskToggleView.as_view(), name="task-toggle"),
    path("task/tags/", TagListView.as_view(), name="tag-list"),
    path("task/tags/create", TagCreateView.as_view(), name="tag-create"),
    path("task/tags/<int:pk>/update/", TagUpdateView.as_view(), name="tag-update"),
    path("task/tags/<int:pk>/delete/", TagDeleteView.as_view(), name="tag-delete"),
]
