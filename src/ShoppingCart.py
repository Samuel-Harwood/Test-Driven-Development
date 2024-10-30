from typing import List

from CartItem import CartItem
from Customer import Customer
from DiscountService import DiscountService

class ShoppingCart:
    def __init__(self, customer: Customer, discount_service: DiscountService):
        self._customer = customer
        self._items: List[CartItem] = []
        self._discount_service = discount_service
        self._coupon_code = None
        self._is_promotion_active = False  # Default promotion status is inactive

    # Add an item to the shopping cart
    def add_item(self, item: CartItem):
        self._items.append(item)

    # Remove an item from the shopping cart
    def remove_item(self, item: CartItem):
        self._items.remove(item)

    # Set a coupon code for discount
    def apply_coupon_code(self, coupon_code: str):
        self._coupon_code = coupon_code

    # Activate or deactivate a promotion
    def set_promotion_active(self, is_active: bool):
        self._is_promotion_active = is_active

    # Calculate the total price before any discounts
    def calculate_total(self) -> float:
        total = sum(item.get_product().get_price() * item.get_quantity() for item in self._items)
        return total

    # Calculate the final price after applying discounts, promotions, and coupon codes
    def calculate_final_price(self) -> float:
        total = self.calculate_total()


        # Apply promotion if active
        if self._is_promotion_active:
            total = self._discount_service.apply_promotion_discount(total)
        else:
            # Apply multi-tier discount, customer type discount, and bundle discount
            total = self._discount_service.apply_discount(total, self._customer.get_customer_type(), self._items, self._coupon_code)

        return total

    # Print a detailed breakdown of the cart
    def print_receipt(self):
        print("----- Shopping Cart Receipt -----")
        for item in self._items:
            print(f"{item.get_product().get_name()} - {item.get_quantity()} x ${item.get_product().get_price():.2f}")
        print("---------------------------------")
        print(f"Total before discount: ${self.calculate_total():.2f}")
        print(f"Final price after discounts: ${self.calculate_final_price():.2f}")

    def get_items(self) -> List[CartItem]:
        return self._items
