from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email address")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "email",
            "first_name",
            "last_name",
        )


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
        )


class WorkerPositionChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("position",)


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Worker username..."}),
    )


class PositionSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search positions..."}),
    )
