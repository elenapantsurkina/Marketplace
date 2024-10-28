from django.contrib import admin
from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at")
    list_filter = ("created_at",)
    search_fields = ("created_at",)
