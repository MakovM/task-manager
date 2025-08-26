from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic

from tasks.forms import TaskForm
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


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.select_related(
        "task_type",
        "created_by"
    ).prefetch_related(
        "assignees",
        "tags"
    )


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:task-list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"

    def get_success_url(self):
        return reverse("tasks:task-detail", kwargs={"pk": self.object.pk})

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.created_by or self.request.user.is_superuser