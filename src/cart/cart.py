class Cart:
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            print('product already in cart')

        else:    
            self.cart[product_id] = {'price': str(product.price)}
            print('Adding product')

        self.session.modified = True
        print(f'self.cart {self.cart}')

    def get_prod_ids(self):
        return self.cart.keys()