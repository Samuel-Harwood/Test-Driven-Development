class CartItem:

    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def get_product(self):
        return self.product

    def get_quantity(self):
        return self.quantity

    def get_total_price(self):
        return self.product.get_price() * self.quantity
