from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from tasks.models import Task


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "tasks/task_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = Task.objects.select_related(
            "task_type"
        ).prefetch_related(
            "assignees",
            "tags"
        )

        comp = self.request.GET.get("comp")
        if comp == "1":
            queryset = queryset.filter(is_completed=True)
        elif comp == "0":
            queryset = queryset.filter(is_completed=False)

        my = self.request.GET.get("my")
        if my == "1":
            queryset = queryset.filter(assignees=self.request.user)

        return queryset


class TaskDetailView(generic.DetailView):
    model = Task
    queryset = Task.objects.select_related(
        "task_type",
        "created_by"
    ).prefetch_related(
        "assignees",
        "tags"
    )
