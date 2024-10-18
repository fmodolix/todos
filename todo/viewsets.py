"""Viewsets for TodoModel."""

from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import TodoModel
from .serializers import (
    TodoCreateSerializer,
    TodoDetailSerializer,
    TodoListSerializer,
    TodoDeleteSerializer,
    TodoCountSerializer,
    TodoInvalidArgument,
)


@extend_schema_view(
    list=extend_schema(
        summary=_("List todos"),
        operation_id="List todos",
        description="List all todos",
        responses={200: TodoListSerializer},
        tags=["todos"],
    )
)
class TodoViewSet(viewsets.ModelViewSet):

    def get_serializers(self, *__, **kwargs):
        if self.request.method.lower() in ["post", "put", "patch"]:
            return TodoCreateSerializer
        elif self.request.method.lower() == "get":
            if "pk" in kwargs:
                return TodoDetailSerializer
            else:
                return TodoListSerializer
        elif self.request.method.lower() == "delete":
            return TodoDeleteSerializer
        return TodoListSerializer

    @extend_schema(
        summary=_("Create a new action item"),
        operation_id="Create todo",
        description="Create a new todo item with a name and description",
        parameters=[
            TodoCreateSerializer,
        ],
        responses={201: TodoDetailSerializer, 400: TodoInvalidArgument},
        tags=["todos"],
    )
    def create(self, request, *args, **kwargs):
        tcs = TodoCreateSerializer(data=request.data)
        if tcs.is_valid():
            todo = tcs.save(created_by=request.user)
            ts = TodoDetailSerializer(todo)
            return Response(
                ts.data, status=status.HTTP_201_CREATED, content_type="application/json"
            )
        else:
            tis = TodoInvalidArgument(tcs.errors)
            return Response(
                tis.data,
                status=status.HTTP_400_BAD_REQUEST,
                content_type="application/json",
            )

    @extend_schema(
        summary=_("Count todos"),
        operation_id="Count todos",
        description="Count all todos",
        responses={200: TodoCountSerializer},
        tags=["todos"],
    )
    @action(methods=["GET"], detail=False, url_path="count", url_name="count")
    def count(self, __):
        return {"count": TodoModel.objects.count()}
