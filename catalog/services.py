from catalog.models import Product, Category
from django.core.cache import cache
from django.shortcuts import get_object_or_404


def get_products_by_category(category_id):

    """Возвращает список всех продуктов в указанной категории с использованием кеширования."""

    cache_key = f'products_category_{category_id}'
    products = cache.get(cache_key)
    if products is None:
        category = get_object_or_404(Category, id=category_id)
        products = category.products.all()
        cache.set(cache_key, products, timeout=300)
    return products
