from django.views.generic import (
    ListView,
    TemplateView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView,
)
from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import Product, Category
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.forms import inlineformset_factory
from catalog.services import get_products_by_category
from django.core.cache import cache
from django.shortcuts import get_object_or_404, render


class ProductListView(ListView):
    model = Product

    # def get_queryset(self):
    #     products = cache.get("products")
    #     if not products:
    #         products = Product.objects.all()
    #         cache.set("products", products, 60)
    #         return products


class ProductCategoryListView(ListView):
    model = Category
    template_name = "catalog/products_category_list.html"
    context_object_name = 'cat_list'

    # def get_queryset(self):
    #     category_id = self.request.GET.get("category")
    #     if not category_id:
    #         return Product.objects.none()
    #     category = get_object_or_404(Category, id=category_id)
    #     return get_products_by_category(category.id)

def get_catgory_list(request):
    cat_list = Category.objects.all()
    return render(request, "catalog/products_category_list.html", {"cat_list":  cat_list})

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
