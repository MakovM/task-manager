from django.shortcuts import render
from django.views import generic

from tasks.models import Task


class TaskListView(generic.ListView):
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

        return queryset