import sys, os
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from ShoppingCart import ShoppingCart
from Customer import Customer
from DiscountService import DiscountService
from CustomerType import CustomerType
from CartItem import CartItem
from Product import Product


#Test suite for the basic functionality of Shopping Cart, 
#More complex methods are tested in test_systemRequirements
class TestShoppingCart(unittest.TestCase):
    def setUp(self):
        self.customer = Customer("Samuel Harwood", CustomerType.REGULAR)
        self.discount_service = DiscountService()
        self.cart = ShoppingCart(self.customer, self.discount_service)
        self.product = Product("something worth 10 dollars", 10.0, 20)
        self.cart_item = CartItem(self.product, 1)


    def test_add_item(self):
        self.cart.add_item(self.cart_item)
        self.assertIn(self.cart_item, self.cart.get_items())

    #There needs to be some check when trying to add an out of stock item to cart, in possible edge cases where an item goes out of stock just as it is added to cart
    def test_add_erroneuos_item(self):
        product = Product("out of stock product", 5.0, 0) #Out of stock
        with self.assertRaises(ValueError, msg="ValueError should be raised. product is out of stock"):
            self.cart.add_item(product)

    def test_remove_item(self):
        self.cart.add_item(self.cart_item)
        self.assertIn(self.cart_item, self.cart.get_items()) #Same as test_add_item
        self.cart.remove_item(self.cart_item) #The last method to test for maximum test coverage
        self.assertNotIn(self.cart_item, self.cart.get_items()) 


    #Try removing an item not in the cart
    def test_remove_non_existant_item(self):
        with self.assertRaises(ValueError):
            self.cart.remove_item(self.cart_item) 


    #This is tested elswhere but it is good to have avery basic test for this method as it is used quite alot
    def test_calculate_total(self): 
        self.cart.add_item(CartItem(Product("Laptop", 1000, 5), 1)) #One laptop
        self.cart.add_item(CartItem(Product("Mouse", 25, 10), 1)) #one Mouse
        expected_value = 1025
        self.assertEqual(self.cart.calculate_total(), expected_value, "Total should be 1025")


    #I chose not to create tests for apply coupon code and set promotion active, as i am unsure how I would prove they function as intended
    #The remaining methods are more heavily tests in test_system_requirements