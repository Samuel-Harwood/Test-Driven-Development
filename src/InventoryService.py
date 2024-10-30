class InventoryService:

    def update_stock(self, item):
        product = item.get_product()
        try:
            product.reduce_stock(item.get_quantity())
        except ValueError:
            raise RuntimeError(f"Failed to update stock for product: {product.get_name()}")
