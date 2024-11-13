import unittest
import sys, os
#Why was the hardest step importing the classes!
#Added extra path to settings.json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from Product import Product


class TestProducts(unittest.TestCase):

   #Some basic setup of two different products
   def setUp(self):
      self.product_one = Product("Test Product", 4.99, 50) #In Stock product
      self.product_two = Product("Test Product 2", 9.99, 0) #Sold out product
       


   
   #Creating products which should not exist. Negative price or negative stock This is not checked by the program,
   #perhaps a bit obvious but still important to note, and a good possible addition to the program!
   def test_product_creation_invalid_price(self):
      with self.assertRaises(ValueError, msg="Creating product with negative price should raise ValueError"):
         Product("Invalid Product", -5.99, 10)
   
   def test_product_creation_invalid_stock(self):
      with self.assertRaises(ValueError, msg="Creating product with negative stock should raise ValueError"):
         Product("Invalid Product", 5.99, -10)


   #This is to test if having two products with the same name, price and stock will be an issue
   #I know this will fail, but i think that this should be checked which is why im making a test for it
   def test_product_creation_invalid_name(self):
      with self.assertRaises(ValueError, msg="Product already exists"):
         new_product = Product("Test Product", 4.99, 50)


   #Testing getters, all added as one to improve readability
   def test_getters(self):
      #Getter getname
      self.assertEqual(self.product_one.get_name(), "Test Product", "name of product is wrong") #These are just to improve code coverage
      self.assertNotEqual(self.product_two.get_name(), "Wrong Product", "name of product2 is wrong")

      #Getter getprice
      self.assertEqual(self.product_one.get_price(), 4.99, "Price of product")
      self.assertNotEqual(self.product_one.get_price(), 9.99, "Price of product is not 9.99")

      #Getter getstock
      self.assertEqual(self.product_one.get_stock(), 50, "Available stock of product") 
      self.assertNotEqual(self.product_two.get_stock(), 50, "Available stock of second product is not 50")


   #Setter setstock and verifying with Getter getstock
   def test_set_get_stock(self):
      #verify initial values
      self.assertEqual(self.product_one.get_stock(), 50, "Initial stock should be 50")
      self.assertEqual(self.product_two.get_stock(), 0, "Initial stock should be 0")

      self.product_one.set_stock(30)#Set new values
      self.assertEqual(self.product_one.get_stock(), 30, "Available stock of product should be 30") #Assert the set_stock worked
      
      self.product_two.set_stock(200)
      self.assertEqual(self.product_two.get_stock(), 200, "Available stock of second product is 200")


   #These tests WILL fail. As there is no error handling for if the stock is set to a negative number
   def test_set_get_stock_fail(self):
      self.product_one.set_stock(-30)
      self.assertEqual(self.product_one.get_stock(), -30) #This should not be possible, but doesn't cause an issue!
      with self.assertRaises(ValueError, msg="Setting stock to a negative value should raise ValueError"):
         self.product_two.set_stock(-200) #This fails because an error is not raised


   #Reducing the stock of a product to valid and invalid values
   def test_reduce_stock(self):
      self.product_one.reduce_stock(10) #valid
      self.assertEqual(self.product_one.get_stock(), 40, "Available stock reduced by 10")

      self.product_one.reduce_stock(40) #valid (verifies previous reduce_stock)
      self.assertEqual(self.product_one.get_stock(), 0, "Available stock reduced by 40")

      with self.assertRaises(ValueError, msg="Reducing stock to a negative value should raise ValueError"):
         self.product_one.reduce_stock(1) #invalid (from 0 to -1)


   #Did not expect this to pass, it seems with a non-int type, the stock just remains the same.
   def test_reduce_stock_invalid_input(self):
      with self.assertRaises(TypeError, msg="Reducing stock with a non-integer value should raise TypeError"):
         self.product_two.reduce_stock("-1") #invalid type
      self.assertEqual(self.product_one.get_stock(), 50, "Stock should remain unchanged after invalid input.") #Im not sure if this passing is good or bad


 



   