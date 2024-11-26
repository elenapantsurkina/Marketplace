from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import ProductListView
from catalog.views import ContactsView
from catalog.views import (
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView, ProductCategoryListView,
    get_catgory_list
)
from django.views.decorators.cache import cache_page


app_name = CatalogConfig.name


urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("category/", ProductCategoryListView.as_view(), name="products_category_list"),
    #path("category/", get_catgory_list, name="products_category_list"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path(
        "product_detail/<int:pk>/", cache_page(60)(ProductDetailView.as_view()), name="product_detail"
    ),
    path(
        "product_delete/<int:pk>/",
        ProductDeleteView.as_view(),
        name="product_delete",
    ),
    path(
        "product_update/<int:pk>/", ProductUpdateView.as_view(), name="product_update"
    ),
    path("product_create/", ProductCreateView.as_view(), name="product_create"),
]
