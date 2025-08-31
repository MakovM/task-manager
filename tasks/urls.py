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
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/<int:pk>/toggle/", TaskToggleView.as_view(), name="task-toggle"),
    path("tasks/tags/", TagListView.as_view(), name="tag-list"),
    path("tasks/tags/create", TagCreateView.as_view(), name="tag-create"),
    path("tasks/tags/<int:pk>/update/", TagUpdateView.as_view(), name="tag-update"),
    path("tasks/tags/<int:pk>/delete/", TagDeleteView.as_view(), name="tag-delete"),
]
