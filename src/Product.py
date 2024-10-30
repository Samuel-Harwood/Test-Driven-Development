class Product:
    def __init__(self, name: str, price: float, stock: int):
        self._name = name
        self._price = price
        self._stock = stock

    # Getters
    def get_name(self) -> str:
        return self._name

    def get_price(self) -> float:
        return self._price

    def get_stock(self) -> int:
        return self._stock

    # Setter
    def set_stock(self, stock: int):
        self._stock = stock

    # Method to reduce stock
    def reduce_stock(self, quantity: int):
        if quantity > self._stock:
            raise ValueError("Not enough stock available")
        self._stock -= quantity
