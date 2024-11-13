import unittest
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from Customer import Customer
from CustomerType import CustomerType


#This test class exists only to improve test coverage. I imagine most of these tests to pass (update: they all do)
class TestCustomer(unittest.TestCase):
    def setUp(self):
      self.customer_one = Customer("Samuel Harwood", CustomerType.REGULAR)
      self.customer_two = Customer("Sam Harwood", CustomerType.VIP)
      self.customer_three = Customer("Samuel H", CustomerType.PREMIUM)


    def test_invalid_customer_type(self):
      with self.assertRaises(ValueError):
         customer_fail = Customer("Samuel H", "PREMIUM") #Creating a customer with an invalid type raises an error

   #testing getters
    def test_get_name(self):
         self.assertEqual(self.customer_one.get_name(), "Samuel Harwood", msg = "names do not match")

    def test_get_customer_type(self):
       self.assertEqual(self.customer_two.get_customer_type(), CustomerType.VIP)

    def test_set_get_name(self):
       self.customer_three.set_name("Not Samuel H")
       self.assertEqual(self.customer_three.get_name(), "Not Samuel H", msg = "names do not match")
  
    def test_set_customer_type(self):
       self.customer_one.set_customer_type(CustomerType.PREMIUM) #Change customer type and verify successful
       self.assertEqual(self.customer_one.get_customer_type(), CustomerType.PREMIUM, msg = "Customer types do not match")

