from django.shortcuts import get_object_or_404
from products.models import Product, ProductImage
from django.db.models import Prefetch


def fetch_products_from_db(ids_filter):
    prefetch_product_imgs = Prefetch(
        'images',
        queryset=ProductImage.objects.only(
            'product', 'image', 'primary_image'
        ).filter(primary_image=True)
    )

    cart_products = Product.objects.only(
        'name', 'size', 'price', 'quantity', 'discount_percentage', 'slug')\
            .prefetch_related(prefetch_product_imgs).filter(id__in=ids_filter)

    return cart_products


def create_context(cart_products, cart):
    cart_product_ids = [product.id for product in cart_products]
    product_quantities = cart.get_product_quantities(cart_product_ids)

    products_data = zip(cart_products, product_quantities)
    subtotal = cart.calculate_subtotal()

    context = {'products_data': products_data, 'subtotal': subtotal}

    return context