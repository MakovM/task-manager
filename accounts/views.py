from django.contrib.auth import get_user_model
from django.urls import reverse_lazy, reverse
from django.views import generic

from accounts.forms import SignUpForm

User = get_user_model()


class SignUpView(generic.CreateView):
    model = User
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("accounts:login")


class WorkerListView(generic.ListView):
    model = User
    context_object_name = "worker_list"
    template_name = "accounts/worker_list.html"
    queryset = User.objects.select_related("position")
    paginate_by = 5


class WorkerDetailView(generic.DetailView):
    model = User
