
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

class testInventoryService(unittest.TestCase):
    def setUp(self):
        self.payment_service = MagicMock(spec=PaymentService)
        self.inventory_service = MagicMock(spec=InventoryService)
        self.order_service = OrderService(self.payment_service, self.inventory_service)
        
        #Creating the customer
        self.customer = Customer("Samuel Harwood", CustomerType.REGULAR)
        self.discount_service = DiscountService()
        self.cart = ShoppingCart(self.customer, self.discount_service)

        #Creating the product and adding to cart
        self.product = Product("MacBook Pro", 1000, 50) #I just copied this from OrderService
        self.cart.add_item(CartItem(self.product, 1))
        self.credit_card_number = "1234567890123456" #Creating credit card, don't steal my number!

    #The same as the previous 
    def test_failed_order_not_update_stock(self):
        self.order_service.place_order(self.cart, self.credit_card_number)
        self.payment_service.process_payment.return_value = False #if payment fails
        self.inventory_service.update_stock.assert_not_called() #This shouldn't be called

    #Trying to get the runtimeError to raise by buying more than there is stock
    def test_insufficient_stock_raises_runtime_error(self):
        inventory_service = InventoryService()  # Use the actual InventoryService, not a mock  
        product = Product("almost out of stock product", 5.99, 3)  # Product with only 3 in stock
        cart_item = CartItem(product, 5)  # Trying to buy 5, which exceeds available stock
        with self.assertRaises(RuntimeError): 
            inventory_service.update_stock(cart_item)

