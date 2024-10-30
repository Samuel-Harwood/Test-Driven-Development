import threading

from ShoppingCart import ShoppingCart

class OrderService:
    def __init__(self, payment_service: 'PaymentService', inventory_service: 'InventoryService'):
        self._payment_service = payment_service
        self._inventory_service = inventory_service
        self._order_lock = threading.Lock()  # Lock for thread safety

    def place_order(self, cart: ShoppingCart, credit_card_number: str) -> bool:
        with self._order_lock:  # Ensure only one thread places an order at a time
            try:
                # Check stock and update it
                for item in cart.get_items():
                    self._inventory_service.update_stock(item)

                # Apply discounts and process payment
                total = cart.calculate_total()
                return self._payment_service.process_payment(credit_card_number, total)
            except Exception as e:
                print(f"Order failed: {e}")
                return False
