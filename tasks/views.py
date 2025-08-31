from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from tasks.forms import TaskForm, TagSearchForm, TaskSearchForm
from tasks.models import Task, Tag

User = get_user_model()


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "tasks/task_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Task.objects.select_related("task_type").prefetch_related(
            "assignees", "tags"
        )

        scope = self.request.GET.get("scope")
        if scope == "my":
            queryset = queryset.filter(assignees=self.request.user)

        status = self.request.GET.get("status")
        if status == "closed":
            queryset = queryset.filter(is_completed=True)
        elif status == "open":
            queryset = queryset.filter(is_completed=False)

        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])

        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.select_related(
        "task_type",
        "created_by"
    ).prefetch_related(
        "assignees", "tags"
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

    def get_object(self):
        if self._cached_object is None:
            self._cached_object = super().get_object()
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

    def get_object(self):
        if self._cached_object is None:
            self._cached_object = super().get_object()
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

        is_assignee = task.assignees.filter(id=request.user.id).exists()

        if (
            request.user == task.created_by
            or request.user.is_staff
            or is_assignee
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TagSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Tag.objects.all()
        form = TagSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


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
