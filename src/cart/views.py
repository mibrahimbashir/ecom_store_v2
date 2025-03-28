from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.db.models import Prefetch
from products.models import Product
from .cart import Cart
from products.models import Product, ProductImage
from .utils import calculate_subtotal


def cart_summary(request):
    cart = Cart(request)

    cart_data = cart.cart_data()

    product_ids = [int(pk) for pk in cart_data.keys()]

    product_images_prefetch = Prefetch(
        'images',
        queryset=ProductImage.objects.only(
            'product',
            'image',
            'primary_image'
        ).filter(primary_image=True)
    )

    products = Product.objects.only(
        'name', 'size', 'price', 'quantity', 'discount_percentage', 'slug') \
            .prefetch_related(product_images_prefetch) \
                .filter(id__in=product_ids)
    
    product_quantities = [cart_data[str(product.id)] for product in products]

    products_data = zip(products, product_quantities)
    subtotal = calculate_subtotal(products, product_quantities)

    context = {'products_data': products_data, 'subtotal': subtotal}

    return render(request, 'cart/cart_summary.html', context)


def cart_add(request, slug):
    cart = Cart(request)

    product = get_object_or_404(Product, slug=slug)

    cart.add(product_id=product.id)
    
    cart_data = cart.cart_data()

    product_ids = [int(pk) for pk in cart_data.keys()]

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
                .filter(id__in=product_ids)
    
    product_quantities = [cart_data[str(product.id)] for product in products]

    products_data = zip(products, product_quantities)
    subtotal = calculate_subtotal(products, product_quantities)

    context = {'products_data': products_data, 'subtotal': subtotal}


    return render(request, 'cart/cart_inline.html', context)


def update_quantity(request, slug):
    return HttpResponse()