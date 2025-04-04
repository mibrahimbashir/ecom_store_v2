from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
import json
from cart.cart import Cart
from products.models import Product


@receiver(user_logged_in)
def load_old_cart(sender, user, request, **kwargs):
    cart = Cart(request)
    if user.cart:
        try:
            # Convert the stored data to a dictionary.
            user_cart = json.loads(user.cart)

            for key, value in user_cart.items():
                product = Product.objects.get(id=int(key))
                cart.db_add(product, quantity=value['quantity'])
                cart.update_user_cart()
        except json.JSONDecodeError as e:
            user_cart = user.cart
