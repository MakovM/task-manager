from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views import generic

from accounts.forms import SignUpForm

User = get_user_model()

class SignUpView(generic.CreateView):
    model = User
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("accounts:login")
