from django.urls import path
from blog.apps import BlogConfig
from blog.views import BlogListView
from blog.views import BlogCreateView
from blog.views import BlogDeleteView
from blog.views import BlogDetailView
from blog.views import BlogUpdateView

app_name = BlogConfig.name

urlpatterns = [
    path("", BlogListView.as_view(), name="blog_list"),
    path("blog_detail/<int:pk>/", BlogDetailView.as_view(), name="blog_detail"),
    path("blog_delete/<int:pk>/", BlogDeleteView.as_view(), name="blog_delete"),
    path("blog_create/", BlogCreateView.as_view(), name="blog_create"),
    path("blog_update/<int:pk>/", BlogUpdateView.as_view(), name="blog_update"), ]
