def calculate_subtotal(products, product_quantities):
    subtotal = 0

    for product, product_quantity in zip(products, product_quantities):
        if product.on_sale:
            subtotal += product.discounted_price * product_quantity
        else:
            subtotal += product.price * product_quantity
    return subtotal