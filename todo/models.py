import uuid
from logging import getLogger
from typing import Tuple, List

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


def check_user(fun):
    # Check that user is authenticated

    def wrapped(user: User, *args, **kwargs):
        if user is not User or not user.is_authenticated:
            logger = getLogger()
            logger.warning(f"Invalid user {user}")
            return None, False

    return wrapped


class TodoModel:
    pass


class TodoManager(models.Manager):

    @check_user
    def get_queryset(self) -> models.QuerySet:
        """Filter on non deleted tasks."""
        return super().get_queryset().filter(deleted_at__isnull=True)

    @check_user
    def create_for_user(
        self, user: User, name: str, description: str = None
    ) -> Tuple[TodoModel, bool]:
        try:
            if not name:
                return TodoModel(), False
            todo = self.create(name=name, description=description)
            return todo, True
        except models.IntegrityError:
            return TodoModel(), False

    @check_user
    def update_for_user(
        self, user: User, pk: uuid.UUID, name: str = None, description: str = None
    ) -> Tuple[TodoModel, bool]:
        try:
            updated_fields: List[str] = ["updated_at", "updated_by"]
            todo = self.get(pk=pk)
            if not name and not description:
                return todo, False
            todo.updated_at = timezone.now()
            todo.updated_by = user
            if name:
                updated_fields.append("name")
                todo.name = name
            if description is not None:
                updated_fields.append("description")
                todo.description = description
            todo.save(updated_fields=updated_fields)
            return todo, True
        except TodoModel.DoesNotExist:
            return TodoModel(), False

    def delete_for_user(self, user: User, pk: uuid.UUID) -> bool:
        try:
            updated_fields: List[str] = ["deleted_by", "deleted_at"]
            todo = self.get(pk=pk)
            todo.deleted_by = user
            todo.deleted_at = timezone.now()
            todo.save(updated_fields=updated_fields)
        except TodoModel.DoesNotExist:
            return False


class TodoModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(
        help_text="Summary of the action to perform", max_length=255
    )
    description = models.TextField(
        help_text="Long description of what is expected", null=True, blank=True
    )
    due_date = models.DateField("Optional date for completion", null=True, blank=True)
    assignee = models.ForeignKey(
        User,
        verbose_name="User that is expected to do the action",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="assigned_tasks",
    )
    created_by = models.ForeignKey(
        User,
        verbose_name="User that created the action",
        related_name="created_tasks",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField("Date of creation", auto_now_add=True)
    updated_by = models.ForeignKey(
        User,
        verbose_name="User that updated the action",
        related_name="updated_tasks",
        on_delete=models.CASCADE,
    )
    updated_at = models.DateTimeField(
        "Date of last modification", null=True, blank=True
    )
    deleted_by = models.ForeignKey(
        User,
        verbose_name="User that deleted the action",
        related_name="deleted_tasks",
        on_delete=models.CASCADE,
    )
    deleted_at = models.DateTimeField("Date of deletion", null=True, blank=True)
    objects = TodoManager()
    all_objects = models.Manager()
