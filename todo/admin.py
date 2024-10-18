from django.contrib import admin
from .models import TodoModel


class TodoAdmin(admin.ModelAdmin):
    fields = "__all__"
    readonly_fields = [
        "id",
        "created_at",
        "created_by",
        "updated_ut",
        "updated_by",
        "deleted_at",
        "deleted_by",
    ]


admin.register(TodoModel, TodoAdmin)
