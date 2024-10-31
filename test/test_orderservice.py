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

#Order service takes two values, payment service and inventory service
#We can create Mocks for these inputs in setup
class testOrderService(unittest.TestCase):
    def setUp(self):
        self.payment_service = MagicMock(spec=PaymentService)
        self.inventory_service = MagicMock(spec=InventoryService)
        self.order_service = OrderService(self.payment_service, self.inventory_service)
        
        #Creating the customer
        self.customer = Customer("Samuel Harwood", CustomerType.REGULAR)
        self.discount_service = DiscountService()
        self.cart = ShoppingCart(self.customer, self.discount_service)

        #Creating the product and adding to cart
        self.product = Product("MacBook Pro", 1000, 50)
        self.cart_item = CartItem(self.product, 1) #Add Macbook to cart    
        self.cart.add_item(self.cart_item)

        #Creating credit card, don't steal my number!
        self.credit_card_number = "1234567890123456"


    def test_place_order_success(self):
        #Set payment value and stock value to true
        self.payment_service.process_payment.return_value = True
        self.inventory_service.update_stock.return_value = True

        self.assertTrue(self.order_service.place_order(self.cart, self.credit_card_number))