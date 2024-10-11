from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'Load test data from fixture'
    # help = 'Add test products to the database'

    def handle(self, *args, **kwargs):
        # Удаляем существующие записи
        Product.objects.all().delete()
        Category.objects.all().delete()
        # Добавляем тестовые продукты
        category, _ = Category.objects.get_or_create(
            name='Бытовая химия', 
            description='Средства для уборки'
        )

        products = [
            {'name': 'Synergetic',
             'description': 'Универсальный очиститель',
             'category': category,
             'price': Decimal('200.00'),
             'image': 'img/univer.jpg'},
            {'name': 'Probioneat',
             'description': 'Дизенфецирующее средство',
             'category': category,
             'price': Decimal('200.00'),
             'image': 'img/dez.jpg'},
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added product: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product already exist: {product.name}'))
