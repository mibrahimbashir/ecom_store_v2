from products.models import Product
from storefront.models import UserProfile


class Cart:
    MAX_ALLOWED_QUANTITY = 20
    PRODUCT_ATTRS = {
        'int': ['quantity', 'discount_percentage'],
        'float': ['price', 'discounted_price', 'total_savings'],
        'str': ['size'],
        'bool': ['on_sale']
    }

    def __init__(self, request):
        self.session = request.session
        self.request = request

        cart = self.session.get('cart')

        if 'cart' not in request.session:
            cart = self.session['cart'] = {}

        self.cart = cart

    def __len__(self):
        return len(self.cart.keys())

    def _validate_quantity(self, product, quantity_to_add=1, update=True):
        if not isinstance(product, Product):
            return False, 'Invalid request. Please try again.'
        elif not isinstance(quantity_to_add, int) or quantity_to_add < 0:
            return False, 'Invalid quantity selected.'

        product_id = str(product.id)
        available_stock = product.quantity

        quantity_in_cart = self.cart.get(product_id, {}).get('quantity', 0)

        new_quantity = quantity_in_cart + quantity_to_add if not update else quantity_to_add

        if new_quantity > available_stock:
            return False, 'No more items available.'
        elif new_quantity > Cart.MAX_ALLOWED_QUANTITY:
            message = f'Cannot add more than {Cart.MAX_ALLOWED_QUANTITY} items'
            return False, message

        return True, 'valid'

    def _set_attrs(self, product, ignore_attrs=['quantity']):
        product_id = str(product.id)

        if product_id not in self.cart:
            return

        for dtype, attrs in Cart.PRODUCT_ATTRS.items():
            for attr in attrs:
                if ignore_attrs is not None and attr in ignore_attrs:
                    continue

                value = getattr(product, attr)

                if dtype == 'int':
                    self.cart[product_id][attr] = int(value)
                elif dtype == 'float':
                    self.cart[product_id][attr] = float(value) if value else 0
                elif dtype == 'str':
                    self.cart[product_id][attr] = str(value)
                elif dtype == 'bool':
                    self.cart[product_id][attr] = bool(value)

    def update_quantity(self, product, new_quantity):
        product_id = str(product.id)
        
        if product_id not in self.cart:
            return False, f'An error occured while updating quantity for product {product}. Please make sure that you have already added the product in cart'

        valid_to_add, msg = self._validate_quantity(product, quantity_to_add=new_quantity)

        if not valid_to_add:
            return False, msg
        
        if new_quantity == 0:
            del self.cart[product_id]
            msg = 'Product Deleted'
        else:
            self.cart[product_id]['quantity'] = new_quantity
            msg = 'Quantity updated'
        self.session.modified = True
        return True, msg

    def update_user_cart(self):
        if self.request.user.is_authenticated:
            current_user = UserProfile.objects.filter(id=self.request.user.id)
            old_cart = str(self.cart)
            old_cart = old_cart.replace('\'', '\"')
            old_cart = old_cart.replace('True', 'true')
            old_cart = old_cart.replace('False', 'false')
            current_user.update(cart=old_cart)

    def db_add(self, product, quantity):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {}

        self.cart[product_id]['quantity'] = quantity
        self._set_attrs(product)

        self.session.modified = True

    def add(self, product):
        # no need for extra check for product's dtype
        # _validate_quantity simultaneously checks the dtype
        valid_to_add, message = self._validate_quantity(product, update=False)

        if not valid_to_add:
            return False, message

        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}

        self.cart[product_id]['quantity'] += 1
        self._set_attrs(product)

        self.session.modified = True

        return True, 'Product has been added to the cart.'

    def calculate_subtotal(self):
        subtotal = 0

        for details in self.cart.values():
            price = details.get('price')
            discounted_price = details.get('discounted_price')
            quantity = details.get('quantity')

            if details.get('on_sale', False):
                subtotal += quantity * discounted_price
            else:
                subtotal += quantity * price

        return subtotal

    def get_product_ids(self):
        return list(map(int, self.cart.keys()))

    def get_product_quantities(self, product_ids=None):
        if product_ids is not None and not isinstance(product_ids, list):
            raise TypeError('ids must be of type list')

        if product_ids:
            return [self.cart[str(pid)]['quantity'] for pid in product_ids]
        else:
            return [details['quantity'] for details in self.cart.values()]
