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
        self.cart.add_item(self.cart_item) #Unlike the other test suites, we want to test what happens when placing an order, so we assume there is an item in the cart
        self.credit_card_number = "1234567890123456" #Creating credit card, don't steal my number!



  
    def test_place_order_success(self):
        self.payment_service.process_payment.return_value = True #when payment works
        self.inventory_service.update_stock.return_value = True #and theres stock
        order_service = OrderService(self.payment_service, self.inventory_service)
        self.assertTrue(order_service.place_order(self.cart, self.credit_card_number)) #place an order

        self.payment_service.process_payment.assert_called_once_with(self.credit_card_number, self.cart.calculate_total()) #confirm payment was processed
        self.inventory_service.update_stock.assert_called_once_with(self.cart_item) #and the stock was updated


    @patch('src.PaymentService.PaymentService') #We dont need these patches but it shows we can add them
    @patch('src.InventoryService.InventoryService') 
    def test_place_order_fail(self, mock_inventory_service, mock_payment_service):
        mock_payment_service.process_payment.return_value = False #when payment fails
        order_service = OrderService(mock_payment_service, mock_inventory_service)
        self.assertFalse(order_service.place_order(self.cart, self.credit_card_number)) #place an order
        #And the payment should be called once, but the stock 
        mock_payment_service.process_payment.assert_called_once_with(self.credit_card_number, self.cart.calculate_total()) #confirm payment was processed
        mock_inventory_service.update_stock.assert_not_called()



