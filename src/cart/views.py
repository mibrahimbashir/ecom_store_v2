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
    if success:
        cart.update_user_cart()

    cart_product_ids = cart.get_product_ids()

    cart_products = fetch_products_from_db(ids_filter=cart_product_ids)

    messages.info(request, msg)

    context = create_context(cart_products, cart)

    return render(request, 'cart/cart_inline.html', context)


def update_quantity(request, slug):
    referrer_url = request.META.get('HTTP_REFERER')

    if 'cart-summary' in referrer_url:
        template = 'cart/partials/summary_content.html'
    else:
        template = 'cart/partials/inline_content.html'

    cart = Cart(request)
    product = get_object_or_404(Product, slug=slug)

    def render_cart_with_message(msg=''):
        cart_product_ids = cart.get_product_ids()
        cart_products = fetch_products_from_db(ids_filter=cart_product_ids)
        context = create_context(cart_products, cart)
        messages.info(request, msg)
        return context

    if request.method == 'POST':
        new_quantity = request.POST.get('quantity')
        try:
            new_quantity = int(new_quantity)
        except:
            context = render_cart_with_message('Invalid request. Enter a valid quantity for product')
            return render(request, template, context)

        if new_quantity < 0:
            context = render_cart_with_message('Invalid quantity selected.')
            return render(request, template, context)

        success, msg = cart.update_quantity(product, new_quantity)
        if success:
            cart.update_user_cart()

        if cart.__len__() == 0:
            return render(request, template, {})

        context = render_cart_with_message(msg)

        return render(request, template, context)
