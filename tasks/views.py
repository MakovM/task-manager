from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from tasks.forms import TaskForm
from tasks.models import Task, Tag

User = get_user_model()


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "tasks/task_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = Task.objects.select_related("task_type").prefetch_related(
            "assignees", "tags"
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


class TaskUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.UpdateView
):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    _cached_object = None

    def get_object(self, queryset=None):
        if self._cached_object is None:
            self._cached_object = super().get_object(queryset)
        return self._cached_object

    def get_success_url(self):
        return reverse("tasks:task-detail", kwargs={"pk": self.object.pk})

    def test_func(self):
        task = self.get_object()
        return (
                self.request.user == task.created_by
                or self.request.user.is_staff
        )


class TaskDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DeleteView
):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks:task-list")
    _cached_object = None

    def get_object(self, queryset=None):
        if self._cached_object is None:
            self._cached_object = super().get_object(queryset)
        return self._cached_object

    def test_func(self):
        task = self.get_object()
        return (
                self.request.user == task.created_by
                or self.request.user.is_staff
        )


class TaskToggleView(generic.View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        task = get_object_or_404(Task, pk=pk)
        if (
            request.user == task.created_by
            or request.user.is_staff
            or request.user in task.assignees.all()
        ):
            task.is_completed = not task.is_completed
            task.save()
            return redirect("tasks:task-list")

        return HttpResponseForbidden(
            "You do not have permission to change this task status."
        )


class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    context_object_name = "tag_list"
    template_name = "tasks/tag_list.html"
    paginate_by = 10


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tag
    fields = ("name",)
    template_name = "tasks/tag_form.html"
    success_url = reverse_lazy("tasks:tag-list")


class TagUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Tag
    fields = ("name",)
    template_name = "tasks/tag_form.html"
    success_url = reverse_lazy("tasks:tag-list")


class TagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Tag
    template_name = "tasks/tag_confirm_delete.html"
    success_url = reverse_lazy("tasks:tag-list")
