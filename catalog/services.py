from catalog.models import Product, Category
from django.core.cache import cache


def get_products_by_category(category_id):

    """Возвращает список всех продуктов в указанной категории с использованием кеширования."""

    cache_key = f'products/category/{category_id}'
    products = cache.get(cache_key)
    if products:
        return products
    products = Product.objects.filter(category_id=category_id)
    cache.set(f"products/category/{category_id}", products, 60)
    return products
