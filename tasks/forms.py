from django import forms
from django.contrib.auth import get_user_model

from tasks.models import Tag, Task

User = get_user_model()


class TaskForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple
    )
    assignees = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
            }
        )
    )

    class Meta:
        model = Task
        fields = [
            "name",
            "priority",
            "task_type",
            "deadline",
            "tags",
            "assignees",
            "description",
        ]


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Task name..."}),
    )


class TagSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search tags..."}),
    )
