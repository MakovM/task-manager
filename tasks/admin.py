from django.contrib import admin

from tasks.models import Task, TaskType, Tag


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ("name", "description")
    list_filter = ("tags", "priority", "is_completed")
    list_display = ("name", "priority", "deadline", "is_completed")


admin.site.register(TaskType)
admin.site.register(Tag)
