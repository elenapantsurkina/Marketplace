from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)
from blog.models import Blog
from django.urls import reverse, reverse_lazy


class BlogListView(ListView):
    model = Blog

    def get_queryset(self):
        return super().get_queryset().filter(public=True)


class BlogDetailView(DetailView):
    model = Blog
    fields = ["title", "content", "public"]

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.number_of_views += 1
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
    model = Blog
    fields = ["title", "content", "public", "number_of_views"]
    success_url = reverse_lazy("blog:blog_list")


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ["title", "content", "public", "number_of_views"]
    success_url = reverse_lazy("blog:blog_list")

    def get_success_url(self):
        return reverse("blog:blog_detail", args=[self.kwargs.get("pk")])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy("blog:blog_list")
