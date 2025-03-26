from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.db.models import Prefetch
from products.models import Product
from .cart import Cart
from products.models import Product, ProductImage


def cart_summary(request):
    cart = Cart(request)
    prod_ids = cart.get_prod_ids()

    product_images_prefetch = Prefetch(
        'images',
        queryset=ProductImage.objects.only(
            'product',
            'image',
            'primary_image'
        ).filter(primary_image=True)
    )

    products = Product.objects.only(
        'name', 'size', 'price', 'quantity', 'discount_percentage') \
            .prefetch_related(product_images_prefetch) \
                .filter(id__in=prod_ids)

    context = {'products': products}

    return render(request, 'cart/cart_summary.html', context)


def cart_add(request, slug):
    cart = Cart(request)

    product = get_object_or_404(Product, slug=slug)
    cart.add(product=product)
    
    prod_ids = cart.get_prod_ids()

    product_images_prefetch = Prefetch(
        'images',
        queryset=ProductImage.objects.only(
            'product',
            'image',
            'primary_image'
        ).filter(primary_image=True)
    )

    products = Product.objects.only(
        'name', 'size', 'price', 'quantity', 'discount_percentage') \
            .prefetch_related(product_images_prefetch) \
                .filter(id__in=prod_ids)
    
    context = {'products': products}

    return render(request, 'cart/cart_inline.html', context)
