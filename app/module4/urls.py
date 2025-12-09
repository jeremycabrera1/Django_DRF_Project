from inspect import getmembers, isclass

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ViewSetMixin

from . import views

router = DefaultRouter()
# Automatically find all the ViewSets in views.py and register them
for name, cls in getmembers(views, isclass):
    if issubclass(cls, ViewSetMixin) and cls.__module__ == views.__name__:
        router.register(
            rf"{name.lower().replace('viewset', '')}", cls, basename=name.lower()
        )


urlpatterns = [
    path("api/mod4/", include(router.urls)),
]
