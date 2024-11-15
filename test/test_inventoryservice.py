
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

class TestInventoryService(unittest.TestCase):
    def setUp(self):
        #Mocking payment inventory and order serice
        self.payment_service = MagicMock(spec=PaymentService)
        self.inventory_service = MagicMock(spec=InventoryService)
        self.order_service = OrderService(self.payment_service, self.inventory_service)
        
        self.customer = Customer("Samuel Harwood", CustomerType.REGULAR)
        self.discount_service = DiscountService()
        self.cart = ShoppingCart(self.customer, self.discount_service)

        #SetUp was duplicated from test_orderservice
        self.product = Product("MacBook Pro", 1000, 50) 
        self.cart.add_item(CartItem(self.product, 1))#Assuming that an item has already been placed in the cart
        self.credit_card_number = "1234567890123456" #valid number



    #update_stock is performed without any checks if the payment failed
    #Test will pass when stock does not updated after payment fails
    def test_failed_order_not_update_stock(self):
        self.order_service.place_order(self.cart, self.credit_card_number) 
        self.payment_service.process_payment.return_value = False 
        self.inventory_service.update_stock.assert_not_called() 

    #Trying to get the runtimeError to raise by buying more than there is stock
    def test_insufficient_stock_raises_runtime_error(self):
        inventory_service = InventoryService()    
        product = Product("almost out of stock product", 5.99, 3)  # Product with little stock left
        cart_item = CartItem(product, 5)  # Trying to buy more than available stock
        with self.assertRaises(RuntimeError): 
            inventory_service.update_stock(cart_item) 

