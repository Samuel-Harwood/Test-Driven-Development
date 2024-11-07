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
        self.credit_card_number = "1234567890123456" #Creating credit card, don't steal my number!



    #Just testing how to use mocks :)
    @patch('src.PaymentService.PaymentService') 
    @patch('src.InventoryService.InventoryService')
    #Same as previous function but without using mocks
    def test_place_order_success(self, mock_inventory_service, mock_payment_service):
        #This could be added in the decorator, but everytime i tried it broke
        mock_payment_service.process_payment.return_value = True
        mock_inventory_service.update_stock.return_value = True
        order_service = OrderService(mock_payment_service, mock_inventory_service)
        self.assertTrue(order_service.place_order(self.cart, self.credit_card_number))


        mock_payment_service.process_payment.assert_called_once_with(self.credit_card_number, self.cart.calculate_total())
        mock_inventory_service.update_stock.assert_called_once_with(self.cart_item)



    #Testing the order service when payment fails 
    @patch('src.PaymentService.PaymentService')
    @patch('src.InventoryService.InventoryService')
    def test_payment_fail(self, mock_inventory_service, mock_payment_service):
        # Configure the mock payment to fail
        mock_payment_service.process_payment.return_value = False  
        order_service = OrderService(mock_payment_service, mock_inventory_service)  #Using local order service for the mocks      
        self.assertFalse(order_service.place_order(self.cart, self.credit_card_number))

        #Even thought the payment fails, stock is still being updated? is this expected???
        mock_inventory_service.update_stock.assert_not_called() 
        mock_payment_service.process_payment.assert_not_called(self.credit_card_number, self.cart.calculate_total()) #Proving it was called


        
    #Just to prove it can be done without mocks

    def test_failed_order_not_update_stock(self):
        self.payment_service.process_payment.return_value = False        
        self.assertFalse(self.order_service.place_order(self.cart, self.credit_card_number))
        self.inventory_service.update_stock.assert_not_called() #This shouldn't be called, as the order wasn't placed


    #Test the order service when placing an order for an out of stock item
    def test_insufficient_stock_fail(self):
        self.payment_service.process_payment.return_value = True
        #The side effect means the mock will raise a runtime error when the inventory service is called
        self.inventory_service.update_stock.side_effect = RuntimeError("Out of stock")
        self.assertFalse(self.order_service.place_order(self.cart, self.credit_card_number)) #Make sure an order isn't placed
        self.inventory_service.update_stock.assert_called_once_with(self.cart_item) #Verify update stock was called, and caused the side effect :)




    #When cart is empty, an order shouldnt be able to be placed
    def test_empty_cart(self):
        empty_cart = ShoppingCart(self.customer, self.discount_service) #create an empty cart     
        self.assertFalse(self.order_service.place_order(empty_cart, self.credit_card_number))  # Current implementation would return True for empty cart
        self.payment_service.process_payment.assert_called_once_with(self.credit_card_number, empty_cart.calculate_total())

