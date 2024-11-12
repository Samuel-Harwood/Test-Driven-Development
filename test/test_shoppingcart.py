import sys, os
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from ShoppingCart import ShoppingCart
from Customer import Customer
from DiscountService import DiscountService
from CustomerType import CustomerType
from CartItem import CartItem
from Product import Product


#This is the last test class i made, and the only thing i am yet to test in ShoppingCart is the remove item feature
#So this test suite will just be for the basic functionality of Shopping Cart, the more compled methods are tests in test_systemRequirements
class TestShoppingCart(unittest.TestCase):
    def setUp(self):
        #Boilerplate setup. No mocks here as they aren't neccessary, and would just diminish readability
        self.customer = Customer("Samuel Harwood", CustomerType.REGULAR)
        self.discount_service = DiscountService()
        self.cart = ShoppingCart(self.customer, self.discount_service)

        # Create a product and a cart item
        self.product = Product("10 dollar bank note", 10.0, 20)
        self.cart_item = CartItem(self.product, 1)

    def test_add_item(self):
        self.cart.add_item(self.cart_item)
        self.assertIn(self.cart_item, self.cart.get_items(), "verify item is in the cart")

    def test_remove_item(self):
        self.cart.add_item(self.cart_item)
        self.assertIn(self.cart_item, self.cart.get_items(), "Verify item is in the cart") #Same as test_add_item
        self.cart.remove_item(self.cart_item) #The last thing i needed for maximum test coverage
        self.assertNotIn(self.cart_item, self.cart.get_items(), "item should not be in the cart anymore") #assertNotIn checks the item is not found in cart

    #This is tested elswhere but it is good to have avery basic test for this method as it is used quite alot
    def test_calculate_total(self): 
        self.cart.add_item(CartItem(Product("Laptop", 1000, 5), 1)) #One laptop
        self.cart.add_item(CartItem(Product("Mouse", 25, 10), 1)) #one Mouse
        expected_value = 1025
        self.assertEqual(self.cart.calculate_total(), expected_value, "Total should be 1025")

    #I chose not to create tests for apply coupon code and set promotion active, as i am unsure how I would prove they function as intended

    #The remaining methods are more heavily tests in test_system_requirements