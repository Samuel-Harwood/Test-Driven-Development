import unittest
import sys, os
from unittest.mock import MagicMock, patch
from io import StringIO

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

#ALL THE IMPORTS
from ShoppingCart import ShoppingCart
from Customer import Customer
from DiscountService import DiscountService
from CustomerType import CustomerType
from OrderService import OrderService
from PaymentService import PaymentService
from InventoryService import InventoryService
from CartItem import CartItem
from Product import Product


class TestSystemRequirements(unittest.TestCase):

    def setUp(self):
        self.discount_service = MagicMock(spec=DiscountService)
        self.customer = Customer("Samuel Harwood", CustomerType.REGULAR)
        self.cart = ShoppingCart(self.customer, self.discount_service)
        #Just some sample products
        self.product_one = Product("Laptop", 1000.0, 10)
        self.product_two = Product("Mouse", 25.0, 50)
        self.product_three = Product("Keyboard", 45.0, 20)
        #Added mocks in setup but alot of these tests define discount service locally


#1. The system shall allow users to browse and select products to add to a shopping cart.
    def test_add_products_to_cart(self):
        
        #Browsing/adding to cart
        self.cart.add_item(CartItem(self.product_one, 1))
        self.cart.add_item(CartItem(self.product_two, 2))
        self.cart.add_item(CartItem(self.product_three, 1))

        item = self.cart.get_items() 
        self.assertEqual(len(item), 3)

        self.assertEqual(item[0].get_product().get_name(), "Laptop")
        self.assertEqual(item[0].get_quantity(), 1) 
        self.assertEqual(item[0].get_total_price(), 1000.0)
        
        self.assertEqual(item[1].get_product().get_name(), "Mouse")
        self.assertEqual(item[1].get_quantity(), 2) #check mouse
        self.assertEqual(item[1].get_total_price(), 50.0)

        self.assertEqual(item[2].get_product().get_name(), "Keyboard")
        self.assertEqual(item[2].get_quantity(), 1) #check keyboard
        self.assertEqual(item[2].get_total_price(), 45.0)

    
#2. The system shall calculate the total price of items in the shopping cart before any discounts.
    def test_calculate_total_before_discount(self):
        self.cart.add_item(CartItem(self.product_one, 1))
        self.cart.add_item(CartItem(self.product_two, 1))
        self.cart.add_item(CartItem(self.product_three, 1))

        actual_total = self.cart.calculate_total()
        self.discount_service.apply_promotion_discount.assert_not_called() 
        self.discount_service.apply_discount.assert_not_called() 
        expected_total = 1070 #keyboard + mouse + laptop
        self.assertEqual(actual_total, expected_total, "cart total should be 1070") 


#3. The system shall provide the ability to apply additional bundle discounts (5% off a mouse price if a laptop is also in the cart).
    def test_apply_bundle_discount(self):
        discount_service = DiscountService() 
        cart = ShoppingCart(self.customer, discount_service)
        cart.add_item(CartItem(self.product_one, 1))  # 1 Laptop
        cart.add_item(CartItem(self.product_two, 1))  # 1 Mouse

        cart.set_promotion_active(False) 
        cart.apply_coupon_code("") #I do not understand why but test breaks without this line
        total_before_discount = cart.calculate_total()  
        mouse_discount = self.product_two.get_price() * 0.05  # 5% off Mouse price
        expected_total = total_before_discount - mouse_discount  # £1,023.75

        actual_total = cart.calculate_final_price() 
        self.assertEqual(actual_total, expected_total, msg="cart total should be 1023.75")
       

    #The same test as the previous, but has 2 mice in the cart, which is neccessary in its current implementation to get the mouse discount to activate.
    def test_apply_bundle_discount_with_current_logic(self):
        discount_service = DiscountService() 
        cart = ShoppingCart(self.customer, discount_service)
        #The discount service only works if two laptops are in the cart. they need to be added seperately
        cart.add_item(CartItem(self.product_one, 1))  # 1 laptop
        cart.add_item(CartItem(self.product_one, 1))  #another laptop
        cart.add_item(CartItem(self.product_two, 1))  # 1 Mouse

        cart.set_promotion_active(False)
        cart.apply_coupon_code("")
        total_before_discount = cart.calculate_total()  
        mouse_discount = self.product_two.get_price() * 0.05  # 5% off Mouse price
        expected_total = total_before_discount - mouse_discount  # should be 2023.75

        actual_total = cart.calculate_final_price()
        self.assertEqual(actual_total, expected_total, msg="cart total should be 2023.75") 


      
#4. The system shall apply tiered discounts based on the total cart value, with predefined discount levels (10% for over £1,000, 15% for over £5,000, and 20% for over £10,000).
    def test_apply_tiered_discount_1001(self):
        product = Product("something somewhat expensive", 1001.00, 10) #criteria for 10% discount
        self.cart.add_item(CartItem(product, 1)) 
        discount_service = DiscountService() 
        actual_total = discount_service.apply_discount(product.get_price(), CustomerType.REGULAR, self.cart.get_items(), "") 
        expected_total = product.get_price() * 0.90 #£900.9
        self.assertEqual(actual_total, expected_total) 


    def test_apply_tiered_discount_5001(self):
        product = Product("something expensive", 5001.00, 10)#criteria for 15% discount
        self.cart.add_item(CartItem(product, 1)) 
        discount_service = DiscountService() 
        actual_total = discount_service.apply_discount(product.get_price(), CustomerType.REGULAR, self.cart.get_items(), "") 
        expected_total = product.get_price() * 0.85 #4250.849
        self.assertAlmostEqual(actual_total, expected_total, places = 2) #using almostequal as python has a meltdown caluclating 15% off 5001 (4250.849)

    #After the last two tests, it became obvious the 10% discount was not possible, especially obvious when looking at the discount service logic. 

    # This test is the only way to get 15% in programs current logic.
    def test_apply_tiered_discount_10001(self):
        product = Product("Something really expensive", 10001.00, 10) #criteria for 20% discount
        self.cart.add_item(CartItem(product, 1)) 
        discount_service = DiscountService() 
        actual_total = discount_service.apply_discount(product.get_price(), CustomerType.REGULAR, self.cart.get_items(), "")
        expected_total = product.get_price() * 0.80 #£8000.80
        self.assertEqual(actual_total, expected_total)


#5. The system shall categorize customers into three types: Regular, Premium, and VIP, with Premium customers receiving an additional 5% discount and VIP customers receiving an additional 10% discount on their total.
    def test_regular_customer_discount(self):
        self.cart.add_item(CartItem(self.product_one, 1)) #1 laptop
        discount = DiscountService()
        
        actual_total = discount.apply_discount(self.cart.calculate_total(),self.customer.get_customer_type(),self.cart.get_items(),"")
        expected_total = self.cart.calculate_total() #0% off
        self.assertEqual(actual_total, expected_total)#REGULAR customers get VIP discount

    def test_premium_customer_discount(self):
        self.customer = Customer("Samuel Harwood", CustomerType.PREMIUM) #create a PREMIUM customer
        cart = ShoppingCart(self.customer, DiscountService()) 
        cart.add_item(CartItem(self.product_one, 1)) 
        discount = DiscountService()

        actual_total = discount.apply_discount(cart.calculate_total(),self.customer.get_customer_type(),cart.get_items(),"")
        expected_total = cart.calculate_total() * 0.95 #5% off
        self.assertEqual(actual_total, expected_total)

    def test_vip_customer_discount(self):
        self.customer = Customer("Samuel Harwood", CustomerType.VIP) #create a VIP customer
        cart = ShoppingCart(self.customer, DiscountService()) 
        cart.add_item(CartItem(self.product_one, 1)) 
        discount = DiscountService()

        actual_total = discount.apply_discount(cart.calculate_total(),self.customer.get_customer_type(),cart.get_items(),"")
        expected_total = cart.calculate_total() * 0.90 #10% off
        self.assertEqual(actual_total, expected_total) 

#6. The system shall allow users to enter coupon codes, which can provide additional percentage-based or fixed-amount discounts (10% off with code "DISCOUNT10" or £50 off with code "SAVE50"). 
# Only one coupon code can be applied and the £50 off will be applied before any percentage discounts.
    def test_coupon_code_discount_10(self):
        discount = DiscountService()
        cart = ShoppingCart(self.customer, discount) 
        cart.add_item(CartItem(self.product_one, 1))

        actual_total = discount.apply_discount(cart.calculate_total(),self.customer.get_customer_type(),cart.get_items(),"DISCOUNT10")
        expected_total = cart.calculate_total() * 0.9

        self.assertEqual(actual_total, expected_total) 


    def test_coupon_code_save_50(self):
        discount = DiscountService()
        cart = ShoppingCart(self.customer, discount) 
        cart.add_item(CartItem(self.product_one, 1))

        actual_total = discount.apply_discount(cart.calculate_total(),self.customer.get_customer_type(),cart.get_items(),"SAVE50")
        expected_total = cart.calculate_total() - 50 

        self.assertEqual(actual_total, expected_total) 


    #Testing SAVE50 coupon on a product < $50
    def test_coupon_code_save_50_edge_case(self):
        discount = DiscountService()
        cart = ShoppingCart(self.customer, discount) 
        cheap_product = Product("PEZ dispenser", 49.00, 10) 
        cart.add_item(CartItem(cheap_product, 1))
        #To solve this, the program should check the carts total is above a certain threshold before adding discounts
        with self.assertRaises(ValueError, msg="Applying a discount to reduce the price below zero should raise ValueError"):
            discount.apply_discount(cart.calculate_total(),self.customer.get_customer_type(),cart.get_items(),"SAVE50") #Use save50 discount


#7. The system shall support time-limited promotions that can be activated or deactivated to apply a flat discount (25% off during a promotional event). 
    def test_time_limited_promotions(self):
        discount = DiscountService()
        cart = ShoppingCart(self.customer, discount)
        cart.add_item(CartItem(self.product_one, 1))
        cart.set_promotion_active(True)

        actual_total = cart.calculate_final_price()
        expected_value = cart.calculate_total() * 0.75 #25% discount
        
        self.assertEqual(actual_total, expected_value)


#8. The discounts listed in points 3 to 7 are applied on top of each other in the order they have been specified. 
    def test_apply_multiple_discounts(self):
        self.customer = Customer("Samuel HArwood", CustomerType.VIP)  # VIP customer
        self.cart = ShoppingCart(self.customer, DiscountService())
        self.cart.add_item(CartItem(self.product_one, 1))  # 1 Laptop
        self.cart.add_item(CartItem(self.product_two, 1))  # 1 Mouse (5% discount)
        
        self.cart.apply_coupon_code("DISCOUNT10")  # 10% off
        self.cart.set_promotion_active(True) #25% off

        total_before_discounts = self.cart.calculate_total()  # Should be 1025.00

        # Calculate the expected final price step by step
        mouse_discount = self.product_two.get_price() * 0.05  # 5% off Mouse price
        total_after_mouse_discount = total_before_discounts - mouse_discount  # Apply mouse discount
        vip_discount = total_after_mouse_discount * 0.90  # 10% VIP
        coupon_discount = vip_discount * 0.90  # 10% coupon
        expected_value = coupon_discount * 0.75  # Another 25% off for the promotion ($621.92)

        actual_value = self.cart.calculate_final_price() #10% coupon, %5 off mouse, %10 VIP, 

        self.assertAlmostEqual(actual_value, expected_value, places = 2) 


#9. The system shall print a detailed receipt summarizing the items in the cart, the total price before discounts, and the final price after all applicable discounts. 
    @patch('sys.stdout', new_callable=StringIO)
    def test_print_receipt(self, output):
        #A purchase of a keyboard, with no active discounts or promotions by a REGULAR customer, SHOULD be full price
        discount = DiscountService()
        cart = ShoppingCart(self.customer, discount)
        cart.add_item(CartItem(self.product_three, 1)) #$45

        cart.set_promotion_active(False)
        cart.apply_coupon_code("") 
        cart.print_receipt()
        
        output = output.getvalue()
        self.assertIn("Shopping Cart Receipt", output)
        self.assertIn("Keyboard - 1 x $45.00", output)
        expected_value = 45 #price of keyboard
        
        self.assertIn(f"Total before discount: ${expected_value:.2f}", output)
        self.assertIn(f"Final price after discounts: ${expected_value:.2f}", output) #Final price after discounts: $33.75 (SHOULD BE 45!)


    #Example from the brief
    @patch('sys.stdout', new_callable=StringIO)
    def test_print_receipt_coursework_example(self, output):
        #VIP Customer. 1 laptop £1000 and 1 mouse £100. SAVE50 Coupon. 
        #£574.75 is expected_value
        self.customer = Customer("Samuel Harwood", CustomerType.VIP)  # VIP customer
        cart = ShoppingCart(self.customer, DiscountService())

        # Adding a laptop and mouse to the cart
        cart.add_item(CartItem(self.product_one, 1)) #Laptop
        cart.add_item(CartItem(Product("Mouse", 100, 10), 1)) #Need to make this locally as the price for mouse is defferent in setup

        cart.set_promotion_active(True)
        cart.apply_coupon_code("SAVE50") 
        cart.print_receipt()

        output = output.getvalue()
        self.assertIn("Shopping Cart Receipt", output)
        self.assertIn("Laptop - 1 x $1000.00", output)
        self.assertIn("Mouse - 1 x $100.00", output)
        
         
        expected_before_discount = 1045 # "Before any discounts and the amount will become £1045"
        expected_after_discounts = 574.75 
        self.assertIn(f"Total before discount: ${expected_before_discount:.2f}", output) 
        self.assertIn(f"Final price after discounts: ${expected_after_discounts:.2f}", output)


#10. The system shall display an error message if the credit card number does not meet the 16-digit requirement or if the transaction amount is zero or negative, preventing the transaction from proceeding.
    def test_invalid_card_number(self):
        #Local instantiations to improve test coverage
        payment_service = PaymentService() 
        inventory_service = InventoryService()
        discount_service = DiscountService()
        cart = ShoppingCart(self.customer, discount_service)
        cart.add_item(CartItem(self.product_one, 1))  # Add only this item to the cart
        
        order_service = OrderService(payment_service, inventory_service)
        
        expected_value = order_service.place_order(cart, "1234567891234")  # Invalid card number (14 digits)
        self.assertFalse(expected_value) 


    #This is what is needed for the test to pass, a product with no cost and a credit card not 16 digits long, this test is just to improve code coverage
    def test_card_number_pass(self):
        payment_service = PaymentService() #I am calling these locally just to be safe
        inventory_service = InventoryService()
        discount_service = DiscountService()
        cart = ShoppingCart(self.customer, discount_service)
        product = Product("Flying Pig", 0, 1) 
        cart.add_item(CartItem(product, 1))  
        
        order_service = OrderService(payment_service, inventory_service)

        expected_value = order_service.place_order(cart, "1234567891234")  # Invalid card number (14 digits)
        self.assertFalse(expected_value) 

