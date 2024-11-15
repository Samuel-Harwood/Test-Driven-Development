import unittest
import sys, os
#Why was the hardest step importing the classes!
#Added extra path to settings.json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from Product import Product


class TestProducts(unittest.TestCase):

   #Just testing Product so only products in setup
   def setUp(self):
      self.product_one = Product("Test Product", 4.99, 50) #In Stock product
      self.product_two = Product("Test Product 2", 9.99, 0) #Sold out product



   
   #Testing negative price and negative stock products being handled by the program
   def test_product_creation_invalid_price(self):
      with self.assertRaises(ValueError):
         Product("Invalid Price", -5.99, 10)
   
   def test_product_creation_invalid_stock(self):
      with self.assertRaises(ValueError):
         Product("Invalid Stock", 5.99, -10)


   #Creating a product that already exists, should raise an error 
   def test_product_creation_invalid_name(self):
      with self.assertRaises(ValueError, msg="Product already exists"):
         self.product_one = Product("Test Product", 4.99, 50)


   def test_getters(self):
      #Getter getname
      self.assertEqual(self.product_one.get_name(), "Test Product") #These are just to improve code coverage
      self.assertNotEqual(self.product_two.get_name(), "Wrong Product")

      #Getter getprice
      self.assertEqual(self.product_one.get_price(), 4.99)
      self.assertNotEqual(self.product_one.get_price(), 9.99)

      #Getter getstock
      self.assertEqual(self.product_one.get_stock(), 50) 
      self.assertNotEqual(self.product_two.get_stock(), 50)


   #Setter setstock and verifying with Getter getstock
   def test_set_get_stock(self):
      #verify initial values
      self.assertEqual(self.product_one.get_stock(), 50)
      self.assertEqual(self.product_two.get_stock(), 0)

      self.product_one.set_stock(30)
      self.assertEqual(self.product_one.get_stock(), 30)
      
      self.product_two.set_stock(200)
      self.assertEqual(self.product_two.get_stock(), 200)


   #Test setting stock to a negative number
   def test_set_stock_to_negative_value(self):
      with self.assertRaises(ValueError, msg="Setting stock to a negative value should raise ValueError"):
         self.product_two.set_stock(-200)


   #Reducing the stock of a product to valid and invalid values
   def test_reduce_stock_valid_and_invalidvalues(self):
      self.product_one.reduce_stock(10) #valid
      self.assertEqual(self.product_one.get_stock(), 40)

      self.product_one.reduce_stock(40) #valid (verifies previous reduce_stock)
      self.assertEqual(self.product_one.get_stock(), 0)

      with self.assertRaises(ValueError):
         self.product_one.reduce_stock(1) #Stock would be -1


   #When inputting a non-int type, stock does not change. Should raise an error IMO 
   def test_reduce_stock_invalid_input(self):
      with self.assertRaises(TypeError, msg="Reducing stock with a non-integer value should raise TypeError"):
         self.product_two.reduce_stock("-1") #invalid type
      self.assertEqual(self.product_one.get_stock(), 50) 


 



   