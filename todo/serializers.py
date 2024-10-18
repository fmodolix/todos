"""Todo Serializers."""

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .models import TodoModel


class TodoListSerializer(serializers.ModelSerializer):
    """Serializes a list of TodoModels."""

    class Meta:
        model = TodoModel
        fields = ["pk", "name", "assignee", "due_date"]


def injection_validator(value):
    forbidden_chars = ["<", ">"]
    return [v for v in value if v not in forbidden_chars]


class TodoCreateSerializer(serializers.ModelSerializer):
    """Input serializer for Todo creation."""

    # name = serializers.CharField(help_text="Name of the action, less than 255 chars", validators=[injection_validator])
    # description = serializers.CharField(help_text="Long text description", validators=[injection_validator])

    class Meta:
        model = TodoModel
        fields = ["name", "description"]


class TodoDetailSerializer(serializers.ModelSerializer):
    """Serialize detail view of Todo."""

    class Meta:
        model = TodoModel
        fields = "__all__"


class TodoDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = TodoModel
        fields = []


class TodoCountSerializer(serializers.Serializer):
    count = serializers.IntegerField(label=_("Number of todo items"), read_only=True)


class TodoInvalidArgument(serializers.Serializer):
    error = serializers.JSONField(label="Validation errors")
