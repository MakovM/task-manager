from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views import generic

from accounts.forms import SignUpForm, WorkerUpdateForm

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


class WorkerUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = User
    form_class = WorkerUpdateForm
    template_name = "accounts/worker_form.html"

    def get_success_url(self):
        return reverse_lazy("accounts:worker-detail", kwargs={"pk": self.object.pk})

    def test_func(self):
        return self.request.user == self.get_object()

class WorkerDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = User
    template_name = "accounts/worker_confirm_delete.html"
    success_url = reverse_lazy("accounts:login")

    def test_func(self):
        return self.request.user == self.get_object()
