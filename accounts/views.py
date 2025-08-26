from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from accounts.forms import (
    SignUpForm,
    WorkerUpdateForm,
    WorkerPositionChangeForm
)

User = get_user_model()


class SignUpView(generic.CreateView):
    model = User
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("accounts:login")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = User
    context_object_name = "worker_list"
    template_name = "accounts/worker_list.html"
    queryset = User.objects.select_related("position")
    paginate_by = 5


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    queryset = User.objects.select_related("position")


class WorkerUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.UpdateView
):
    model = User
    form_class = WorkerUpdateForm
    template_name = "accounts/worker_form.html"
    queryset = User.objects.select_related("position")
    _cached_object = None

    def get_object(self, queryset=None):
        if self._cached_object is None:
            self._cached_object = super().get_object(queryset)
        return self._cached_object

    def get_success_url(self):
        return reverse_lazy(
            "accounts:worker-detail",
            kwargs={"pk": self.object.pk}
        )

    def test_func(self):
        return self.request.user == self.get_object()


class WorkerDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DeleteView
):
    model = User
    template_name = "accounts/worker_confirm_delete.html"
    success_url = reverse_lazy("accounts:login")
    queryset = User.objects.select_related("position")
    _cached_object = None

    def get_object(self, queryset=None):
        if self._cached_object is None:
            self._cached_object = super().get_object(queryset)
        return self._cached_object

    def test_func(self):
        return self.request.user == self.get_object()


class WorkerPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "accounts/change_password.html"
    success_url = reverse_lazy("accounts:worker-detail")

    def get_success_url(self):
        return reverse_lazy(
            "accounts:worker-detail", kwargs={"pk": self.request.user.pk}
        )


class WorkerPositionChangeView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.UpdateView
):
    model = User
    form_class = WorkerPositionChangeForm
    template_name = "accounts/worker_form.html"
    queryset = User.objects.select_related("position")
    _cached_object = None

    def get_object(self, queryset=None):
        if self._cached_object is None:
            self._cached_object = super().get_object(queryset)
        return self._cached_object

    def get_success_url(self):
        return reverse_lazy(
            "accounts:worker-detail", kwargs={"pk": self.object.pk}
        )

    def test_func(self):
        return (
                self.request.user.is_staff
                and self.request.user != self.get_object()
        )


class WorkerStatusChangeView(generic.View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        worker = get_object_or_404(User, pk=pk)
        if request.user.is_staff:
            worker.is_staff = not worker.is_staff
            worker.save()
            return redirect("accounts:worker-detail", pk=worker.id)

        return HttpResponseForbidden(
            "You do not have permission to change User status."
        )
