from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from products.models import Product
from .cart import Cart


def cart_add(request, slug):
    print("\nRequest received to add product")

    cart = Cart(request)
    product = get_object_or_404(Product, slug=slug)

    cart.add(product=product)
    
    print()

    return JsonResponse({'Product name': product.name})