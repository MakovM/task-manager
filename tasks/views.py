from django.shortcuts import render
from django.views import generic

from tasks.models import Task


class TaskListView(generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "tasks/task_list.html"
    paginate_by = 5
