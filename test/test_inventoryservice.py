
import unittest
import sys, os
from unittest.mock import MagicMock

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

        #SetUp was duplicated from test_orderservice
        self.product = Product("MacBook Pro", 1000, 50) 
        self.cart.add_item(CartItem(self.product, 1))#Assuming that an item has already been placed in the cart
        self.credit_card_number = "1234567890123456" 



    #I think that the update stock should not be called if process payment returns false
    #In the current implementation, update stock is done first without any checks
    def test_failed_order_not_update_stock(self):
        self.order_service.place_order(self.cart, self.credit_card_number)
        self.payment_service.process_payment.return_value = False #if payment fails
        self.inventory_service.update_stock.assert_not_called() #This shouldn't be called

    #Trying to get the runtimeError to raise by buying more than there is stock
    #Mocks dont make much sense here so most things are defined locally
    def test_insufficient_stock_raises_runtime_error(self):
        inventory_service = InventoryService()  # Use the actual InventoryService, not a mock  
        product = Product("almost out of stock product", 5.99, 3)  # Product with only 3 in stock
        cart_item = CartItem(product, 5)  # Trying to buy 5, which exceeds available stock
        with self.assertRaises(RuntimeError): 
            inventory_service.update_stock(cart_item)

