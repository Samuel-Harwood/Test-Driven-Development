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


class testShoppingCart:

    def setUp(self):
        self.discount_service = Mock(spec=DiscountService)
        self.customer = Customer("Samuel Harwood", CustomerType.REGULAR)
        self.cart = ShoppingCart(self.customer, self.discount_service)
    
   
    