import unittest
import sys, os
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
        #Mocking for payment and inventory service
        self.payment_service = MagicMock(spec=PaymentService)
        self.inventory_service = MagicMock(spec=InventoryService)
        #Not mocking order service, but using mocks in its initalisation
        self.order_service = OrderService(self.payment_service, self.inventory_service)
        
        #Creating the customer
        self.customer = Customer("Samuel Harwood", CustomerType.REGULAR)
        self.discount_service = DiscountService()
        self.cart = ShoppingCart(self.customer, self.discount_service)

        #Creating the product and adding to cart
        self.product = Product("MacBook Pro", 1000, 50)
        self.cart_item = CartItem(self.product, 1) #Add Macbook to cart 
        #We want to test what happens when placing an order, so we assume there is an item in the cart   
        self.cart.add_item(self.cart_item) 
        self.credit_card_number = "1234567890123456" #Creating credit card, don't steal my number!



  
    def test_place_order_success(self):
        self.payment_service.process_payment.return_value = True #when payment works
        self.inventory_service.update_stock.return_value = True #and theres stock
        self.assertTrue(self.order_service.place_order(self.cart, self.credit_card_number)) #place an order

        self.payment_service.process_payment.assert_called_once_with(self.credit_card_number, self.cart.calculate_total()) #confirm payment was processed
        self.inventory_service.update_stock.assert_called_once_with(self.cart_item) #and the stock was updated

    #The problem with using mocks here is it doesnt account for the incorrect logic in PaymentService
    def test_place_order_fail(self):
        self.payment_service.process_payment.return_value = False #when payment fails
        self.assertFalse(self.order_service.place_order(self.cart, self.credit_card_number)) #An order should not be placed


    #An exmaple of how to go about using patches
    #This code is not complex enough to need these, and as mocks are built-in to our setup..
    #they're not neccessary. But I added them to show how they could be used
    @patch('src.PaymentService.PaymentService') 
    @patch('src.InventoryService.InventoryService') 
    def test_place_order_fail_stock_not_updated(self, mock_inventory_service, mock_payment_service):
        mock_payment_service.process_payment.return_value = False #when payment fails (this could've used self.payment_service)
        order_service = OrderService(mock_payment_service, mock_inventory_service) #Could just be self.payment/inventory.service

        self.assertFalse(order_service.place_order(self.cart, self.credit_card_number)) #Fail to place an order
        mock_payment_service.process_payment.assert_called_once_with(self.credit_card_number, self.cart.calculate_total()) #confirm payment was processed
        mock_inventory_service.update_stock.assert_not_called() #Stock shouldn't be updated if the order isn't placed 
        #self.assertEqual(mock_inventory_service.update_stock.call_count, 2) #(or maybe the stock should be re-updated to original value once failed)


    def test_place_order_empty_cart(self):
        empty_cart = ShoppingCart(self.customer, self.discount_service)  # Create a new, empty cart
        payment_service = PaymentService() #The mocked payment service does not work well with AssertFalse 
        order_service = OrderService(payment_service, self.inventory_service) #define new order service
        self.assertFalse(order_service.place_order(empty_cart, self.credit_card_number)) #This should Fail because the cart has nothing to purchase




