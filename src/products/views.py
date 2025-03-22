from django.shortcuts import render
from .models import Product


def product_page(request, slug):
    product = Product.objects.prefetch_related('images').get(slug=slug)

    context = {'product': product}

    return render(request, 'products/product_page.html', context)