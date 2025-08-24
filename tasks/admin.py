from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import Worker, Position
from tasks.models import Task, TaskType, Tag


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    list_filter = UserAdmin.list_filter + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "position",
                    )
                },
            ),
        )
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ("name", "description")
    list_filter = ("tags", "priority", "is_completed")
    list_display = ("name", "priority", "deadline", "is_completed")


admin.site.register(TaskType)
admin.site.register(Position)
admin.site.register(Tag)
