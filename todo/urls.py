from django.urls import path, include
from rest_framework import routers
from .viewsets import TodoViewSet

router = routers.DefaultRouter(trailing_slash=True)
router.register("todos", TodoViewSet, basename="todos")

urlpatterns = [
    path('', include(router.urls), name='todos'),

]
