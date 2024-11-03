import unittest
import sys, os
from unittest import TestCase
from unittest.mock import MagicMock, patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


from ShoppingCart import ShoppingCart
from Customer import Customer
from DiscountService import DiscountService
from CustomerType import CustomerType
from OrderService import OrderService
from PaymentService import PaymentService
from InventoryService import InventoryService
from CartItem import CartItem
from Product import Product


class testShoppingCart(unittest.TestCase):

    def setUp(self):
        self.discount_service = MagicMock(spec=DiscountService)
        self.customer = Customer("Samuel Harwood", CustomerType.REGULAR)
        self.cart = ShoppingCart(self.customer, self.discount_service)
        #Just some sample products
        self.product_one = Product("Laptop", 1000.0, 10)
        self.product_two = Product("Mouse", 25.0, 50)
        self.product_three = Product("Keyboard", 45.0, 20)

#1. The system shall allow users to browse and select products to add to a shopping cart.
    def test_add_products_to_cart(self):
        
        #I'm assuming this classifies as the browsing part??
        self.cart.add_item(CartItem(self.product_one, 1))
        self.cart.add_item(CartItem(self.product_two, 2))
        self.cart.add_item(CartItem(self.product_three, 1))

        items_in_cart = self.cart.get_items() #Making my life easier
        self.assertEqual(len(items_in_cart), 3, "Cart should contain exactly three items.")

        #checks for laptop
        self.assertEqual(items_in_cart[0].get_product().get_name(), "Laptop")
        self.assertEqual(items_in_cart[0].get_quantity(), 1) 
        self.assertEqual(items_in_cart[0].get_total_price(), 1000.0, "Price for Laptop should be 1000.0")
        #Price could be written as (self.product_one.get_price() *  items_in_cart[0].get_quantity()) but best practice is to keep it static
        #If the behaviour isnt working as intended, then calling the actual methods to calculat it will return true when it should be false
        #does that make sense?
        
        #check for mouse
        self.assertEqual(items_in_cart[1].get_product().get_name(), "Mouse")
        self.assertEqual(items_in_cart[1].get_quantity(), 2) #check mouse
        self.assertEqual(items_in_cart[1].get_total_price(), 50.0, "Price for 2 mice should be 50.0")

        #check for keyboard
        self.assertEqual(items_in_cart[2].get_product().get_name(), "Keyboard")
        self.assertEqual(items_in_cart[2].get_quantity(), 1) #check keyboard
        self.assertEqual(items_in_cart[2].get_total_price(), 45.0, "Price for keyboard should be 47.0")

    



#2. The system shall calculate the total price of items in the shopping cart before any discounts.
    def test_calculate_total_before_discount(self):
        self.cart.add_item(CartItem(self.product_one, 1))
        self.cart.add_item(CartItem(self.product_two, 2))
        self.cart.add_item(CartItem(self.product_three, 1))

        total_before_discount = self.cart.calculate_total()
        self.discount_service.apply_promotion_discount.assert_not_called() #Making sure Mock apply promotion isn't called
        self.discount_service.apply_discount.assert_not_called() #Or Mock apply discount
        expected_total = ((1000 * 1) + (25 * 2) + (45 * 1)) #1095
        self.assertEqual(total_before_discount, expected_total, "Value should be 1095") 

#3. The system shall provide the ability to apply additional bundle discounts (5% off a mouse price if a laptop is also in the cart).
    def test_apply_bundle_discount(self):
        self.cart.add_item(CartItem(self.product_one, 1))  # Laptop
        self.cart.add_item(CartItem(self.product_two, 1))  # Mouse

        total_before_discount = self.cart.calculate_total()  # Expected 1025.0 

        # Calculate the bundle discount (5% off THE MOUSE price)
        mouse_discount = self.product_two.get_price() * 0.05  #1.25
        expected_final_price = total_before_discount - mouse_discount  # 1023.75

        # Mock the apply_discount method to return the correct final price
        self.discount_service.apply_discount = MagicMock(return_value=expected_final_price)

        total_after_discount = self.cart.calculate_final_price()

        self.discount_service.apply_discount.assert_called_once()  # Ensure apply_discount was called once
        self.discount_service.apply_promotion_discount.assert_not_called()  # No promotion
        self.assertAlmostEqual(total_after_discount, expected_final_price, places=2, msg="Value should be 10") #places = 2 because it is a float
      