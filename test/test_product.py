import unittest
import sys, os
#Why was the hardest step importing the classes!
#Added extra path to settings.json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from Product import Product



class TestProducts(unittest.TestCase):


   def setUp(self):
       self.product_one = Product("Test Product", 4.99, 50)
       
   def test_get_name(self):
      self.assertEqual(self.product_one.get_name(), "Test Product", "Check name of product")
   def test_get_price(self):
      self.assertEqual(self.product_one.get_price(), 4.99, "Price of product")
   def test_get_stock(self):
      self.assertEqual(self.product_one.get_stock(), 50, "Available stock of product")
   def test_set_get_stock(self):
      self.product_one.set_stock(30)
      self.assertEqual(self.product_one.get_stock(), 30, "Available stock of product should be 30")
   
   def test_reduce_stock_success(self):
      self.product_one.reduce_stock(10)
      self.assertEqual(self.product_one.get_stock(), 40, "Available stock reduced by 10")
      
   @unittest.expectedFailure
   def test_reduce_stock_fail(self):
      self.product_one.reduce_stock(51) 
      try:
         self.product_one.reduce_stock(51) 
      except ValueError as e:
         self.assertEqual(str(e), "Not enough stock available", "The correct error message should be shown.")
      raise


   def test_reduce_stock_edgecase_fail(self):
      self.product_one.reduce_stock(50)
      self.assertEqual(self.product_one.get_stock(), 0, "Edge case, reducing stock to 0 and then trying to reduce again by 1")
      with self.assertRaises(ValueError):
         self.product_one.reduce_stock(1)

if __name__ == "__main__":
    unittest.main()

   