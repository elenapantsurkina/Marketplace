from django.shortcuts import render

from catalog.models import Product


def home(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, 'products.html', context)


def contacts(request):
    return render(request, 'contacts.html')


# def index(request):
#     return render(request, 'base.html')
