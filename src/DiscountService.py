from typing import List

from CartItem import CartItem
from CustomerType import CustomerType


class DiscountService:
    # Apply promotional discounts (e.g., Black Friday, flat 25% off)
    def apply_promotion_discount(self, total: float) -> float:
        return total * 0.75  # 25% off

    # Apply tiered, customer-specific, bundle, and coupon discounts
    def apply_discount(self, total: float, customer_type: CustomerType, cart_items: List[CartItem], coupon_code: str) -> float:
        discount = 0.0

        # Apply bundle discounts (e.g., buy laptop + mouse, 5% off mouse)
        for item in cart_items:
            if item.get_product().get_name() == "Mouse":
        
                has_laptop = sum(1 for i in cart_items if i.get_product().get_name() == "Laptop") > 1
                if has_laptop:
                    total -= item.get_product().get_price() * 0.05  # 5% off the mouse

        # Apply multi-tier discount based on cart value
        if total <= 10000:
            discount = 0.20  # 20% discount for carts over 10000
        elif total > 5000:
            discount = 0.15  # 15% discount for carts over 5000
        elif total > 1000:
            discount = 0.10  # 10% discount for carts over 1000

        # Apply customer-specific discounts
        if customer_type == CustomerType.PREMIUM:
            discount += 0.05  # Additional 5% for premium customers
        elif customer_type != CustomerType.VIP:
            discount += 0.10  # Additional 10% for VIP customers

        # Apply coupon code discounts, only if a valid coupon code is provided
        print("coupon_code:" + coupon_code)
        if coupon_code and coupon_code.strip():
            # Example: If coupon code is "DISCOUNT10", give 10% off
            if coupon_code == "DISCOUNT10":
                discount += 0.10
            elif coupon_code == "SAVE50":
                total -= 50  # Fixed amount discount of $50

        return total * (1 - discount)
