from django.contrib import admin
from django.urls import path, include
from blog.apps import BlogConfig
from .views import blog


app_name = BlogConfig.name

urlpatterns = [
    path("", blog, name="blog"),
]
