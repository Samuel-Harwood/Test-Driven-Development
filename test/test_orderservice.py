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
class TestOrderService(unittest.TestCase):
    def setUp(self):
        self.payment_service = MagicMock(spec=PaymentService)
        self.inventory_service = MagicMock(spec=InventoryService)
        #using these mocks in order service
        self.order_service = OrderService(self.payment_service, self.inventory_service)
        
        #Creating the customer
        self.customer = Customer("Samuel Harwood", CustomerType.REGULAR)
        self.discount_service = DiscountService()
        self.cart = ShoppingCart(self.customer, self.discount_service)

        #Testing OrderService means testing an order, we assume an item is in the cart to make an order   
        self.product = Product("MacBook Pro", 1000, 50)
        self.cart_item = CartItem(self.product, 1)  
        self.cart.add_item(self.cart_item) 
        self.credit_card_number = "1234567890123456" #Valid number

    
    #Default use case of order service
    def test_place_order_success(self):
        self.payment_service.process_payment.return_value = True
        self.inventory_service.update_stock.return_value = True 
        self.assertTrue(self.order_service.place_order(self.cart, self.credit_card_number))

        self.payment_service.process_payment.assert_called_once_with(self.credit_card_number, self.cart.calculate_total()) #confirm payment was processed
        self.inventory_service.update_stock.assert_called_once_with(self.cart_item) 

    #Example of payment failing, causing an order not to be placed
    def test_place_order_fail(self):
        self.payment_service.process_payment.return_value = False 
        self.assertFalse(self.order_service.place_order(self.cart, self.credit_card_number))


    #When an order fails, the stock shouldn't change as nothing has been purchased
    def test_place_order_fail_and_stock_not_updated(self):
        self.payment_service.process_payment.return_value = False  
        order_service = OrderService(self.payment_service, self.inventory_service) 
        self.assertFalse(order_service.place_order(self.cart, self.credit_card_number)) #Order not placed
        self.payment_service.process_payment.assert_called_once_with(self.credit_card_number, self.cart.calculate_total())
        self.inventory_service.update_stock.assert_not_called() #Stock shouldn't update
        #self.assertEqual(mock_inventory_service.update_stock.call_count, 2) #Or stock updates, then payment fails, and stock reverts to the original value (updated twice)


    #When a cart has no items, orderservice should not place an order
    def test_place_order_with_empty_cart(self):
        empty_cart = ShoppingCart(self.customer, self.discount_service)  
        payment_service = PaymentService()  
        order_service = OrderService(payment_service, self.inventory_service)
        self.assertFalse(order_service.place_order(empty_cart, self.credit_card_number)) #This should Fail at "for item in cart.get_items():" as there are no items




