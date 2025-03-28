from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Prefetch
from django.contrib import messages
from products.models import Product
from .cart import Cart
from cart.utils import fetch_products_from_db, create_context
from products.models import Product, ProductImage


def cart_summary(request):
    cart = Cart(request)

    if cart.__len__() == 0:
        return render(request, 'cart/cart_summary.html')

    cart_product_ids = cart.get_product_ids()

    cart_products = fetch_products_from_db(ids_filter=cart_product_ids)

    context = create_context(cart_products, cart)

    return render(request, 'cart/cart_summary.html', context)


def cart_add(request, slug):
    cart = Cart(request)

    product = get_object_or_404(Product, slug=slug)

    success, msg = cart.add(product)

    cart_product_ids = cart.get_product_ids()

    cart_products = fetch_products_from_db(ids_filter=cart_product_ids)

    messages.info(request, msg)

    context = create_context(cart_products, cart)

    return render(request, 'cart/cart_inline.html', context)


def update_quantity(request, slug):
    # implement later
    return HttpResponse()