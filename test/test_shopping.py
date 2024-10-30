import unittest

#Why was the hardest step importing the classes!
#Added extra path to settings.json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from CartItem import CartItem
from Customer import Customer
from CustomerType import CustomerType
from DiscountService import DiscountService
from InventoryService import InventoryService
from OrderService import OrderService
from PaymentService import PaymentService
from Product import Product
from ShoppingCart import ShoppingCart


class TestShoppingCart(unittest.TestCase):


   def setUp(self):
      #Creating a customer and setting up the environment
      self.customer = Customer("Test Customer", CustomerType.REGULAR)
      self.discount_service = DiscountService()
      self.cart = ShoppingCart(self.customer, self.discount_service)
      self.order_service = OrderService(PaymentService(), InventoryService())
   

   def testEmptyCart(self):
      result = self.order_service.place_order(self.cart, "1234567812345678")
      self.assertFalse(result, "Order should not be placed with an empty cart.")

   def test_print_receipt_empty_cart(self):
        from io import StringIO
        import sys
        
        captured_output = StringIO()
        sys.stdout = captured_output  
        
        self.cart.print_receipt()  
        
        sys.stdout = sys.__stdout__  
        expected_output = "----- Shopping Cart Receipt -----\n---------------------------------\nTotal before discount: $0.00\nFinal price after discounts: $0.00\n"
        self.assertEqual(captured_output.getvalue(), expected_output, "Receipt output for an empty cart should be correct.")



if __name__ == "__main__":
    unittest.main()