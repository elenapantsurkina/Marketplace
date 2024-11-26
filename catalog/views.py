from django.views.generic import (
    ListView,
    TemplateView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView,
)
from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import Product
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.forms import inlineformset_factory
from catalog.services import get_catalog_from_cache


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        return get_catalog_from_cache()


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")

    def test_func(self):
        product = self.get_object()  # Получаем текущий объект продукта
        return self.request.user == product.owner or self.request.user.has_perm(
            "catalog.can_delete_product"
        )

    def handle_no_permission(self):
        return HttpResponseForbidden("Вам запрещено удалять этот продукт.")


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm("catalog.can_unpublish_product"):
            return ProductModeratorForm
        raise PermissionDenied

    def test_func(self):
        product = self.get_object()  # Получаем текущий объект продукта
        return self.request.user == product.owner or self.request.user.has_perm(
            "catalog.can_edit_product"
        )

    def handle_no_permission(self):
        return HttpResponseForbidden("Вам запрещено редактировать этот продукт.")
