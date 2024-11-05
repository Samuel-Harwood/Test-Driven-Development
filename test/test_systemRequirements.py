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


class testSystemRequirements(unittest.TestCase):

    def setUp(self):
        self.discount_service = MagicMock(spec=DiscountService)
        self.customer = Customer("Samuel Harwood", CustomerType.REGULAR)
        self.cart = ShoppingCart(self.customer, self.discount_service)
        #Just some sample products
        self.product_one = Product("Laptop", 1000.0, 10)
        self.product_two = Product("Mouse", 25.0, 50)
        self.product_three = Product("Keyboard", 45.0, 20)



#1. The system shall allow users to browse and select products to add to a shopping cart.
    def test_add_products_to_cart(self):
        
        #I'm assuming this classifies as the browsing part??
        self.cart.add_item(CartItem(self.product_one, 1))
        self.cart.add_item(CartItem(self.product_two, 2))
        self.cart.add_item(CartItem(self.product_three, 1))

        items_in_cart = self.cart.get_items() #Making my life easier
        self.assertEqual(len(items_in_cart), 3, "Cart should contain exactly three items.")

        #checks for laptop
        self.assertEqual(items_in_cart[0].get_product().get_name(), "Laptop")
        self.assertEqual(items_in_cart[0].get_quantity(), 1) 
        self.assertEqual(items_in_cart[0].get_total_price(), 1000.0, "Price for Laptop should be 1000.0")
        #Price could be written as (self.product_one.get_price() *  items_in_cart[0].get_quantity()) but best practice is to keep it static
        #If the behaviour isnt working as intended, then calling the actual methods to calculat it will return true when it should be false
        #does that make sense?
        
        #check for mouse
        self.assertEqual(items_in_cart[1].get_product().get_name(), "Mouse")
        self.assertEqual(items_in_cart[1].get_quantity(), 2) #check mouse
        self.assertEqual(items_in_cart[1].get_total_price(), 50.0, "Price for 2 mice should be 50.0")

        #check for keyboard
        self.assertEqual(items_in_cart[2].get_product().get_name(), "Keyboard")
        self.assertEqual(items_in_cart[2].get_quantity(), 1) #check keyboard
        self.assertEqual(items_in_cart[2].get_total_price(), 45.0, "Price for keyboard should be 47.0")

    



#2. The system shall calculate the total price of items in the shopping cart before any discounts.
    def test_calculate_total_before_discount(self):
        self.cart.add_item(CartItem(self.product_one, 1))
        self.cart.add_item(CartItem(self.product_two, 2))
        self.cart.add_item(CartItem(self.product_three, 1))

        total_before_discount = self.cart.calculate_total()
        self.discount_service.apply_promotion_discount.assert_not_called() #Making sure Mock apply promotion isn't called
        self.discount_service.apply_discount.assert_not_called() #Or Mock apply discount
        expected_total = ((1000 * 1) + (25 * 2) + (45 * 1)) #1095
        self.assertEqual(total_before_discount, expected_total, "Value should be 1095") 

#3. The system shall provide the ability to apply additional bundle discounts (5% off a mouse price if a laptop is also in the cart).
    def test_apply_bundle_discount(self):
        discount_service = DiscountService()
        self.cart = ShoppingCart(self.customer, discount_service)
        self.cart.add_item(CartItem(self.product_one, 1))  # 1 Laptop
        self.cart.add_item(CartItem(self.product_two, 1))  # 1 Mouse

        self.cart.set_promotion_active(False)  # Just making sure no discount is called
        self.cart.apply_coupon_code("") #I do not understand why this is needed but it breaks without it
        total_before_discount = self.cart.calculate_total()  
        mouse_discount = self.product_two.get_price() * 0.05  # 5% off Mouse price
        expected_final_price = total_before_discount - mouse_discount  # should be 1,023.75


        # Call calculate_final_price to trigger the discount logic
        total_after_discount = self.cart.calculate_final_price()

        # Assert that the total after discount is equal to the expected final price
        self.assertAlmostEqual(total_after_discount, expected_final_price, places=2,msg="The discount does not apply as expected for the bundle.")
        #I honestly do not know how the discount is so large for this, could be my mistake
       
        
      
#4. The system shall apply tiered discounts based on the total cart value, with predefined discount levels (10% for over £1,000, 15% for over £5,000, and 20% for over £10,000).
    def test_apply_tiered_discount_1000(self):
        total = self.product_one.get_price()     
        discount_service = DiscountService() #Had to add this locally to get this to work 
        final_total = discount_service.apply_discount(self.product_one.get_price(), CustomerType.REGULAR, self.cart.get_items(), "")
        expected_total = self.product_one.get_price() * 0.90
        self.assertEqual(final_total, expected_total, msg="discount is not equal to 10%") 

    #After the last test, it became obvious the 10% discount was not possible, especially obvious when looking at the discount service logic. 

    # This test is the only way to get 15%.
    def test_apply_tiered_discount_10001(self):
        product = Product("Something really expensive", 10001.00, 10)
        discount_service = DiscountService() #Had to add this locally to get this to work 
        final_total = discount_service.apply_discount(product.get_price(), CustomerType.REGULAR, self.cart.get_items(), "")
        expected_total = product.get_price() * 0.80
        self.assertEqual(final_total, expected_total, msg="discount is not equal to 20%") #Discount is actually 25% currently


#5. The system shall categorize customers into three types: Regular, Premium, and VIP, with Premium customers receiving an additional 5% discount and VIP customers receiving an additional 10% discount on their total.
    def test_regular_customer_discount(self):
        self.cart.add_item(CartItem(self.product_one, 1)) #One laptop
        discount = DiscountService()
        total = discount.apply_discount(total=self.cart.calculate_total(),customer_type=self.customer.get_customer_type(),cart_items=self.cart.get_items(),coupon_code="")
        expected_total = self.cart.calculate_total() #0% off
        #Funnily enough a regular customer is getting the best deal. The 20% meant for large purchases + 10% for VIP
        self.assertAlmostEqual(total, expected_total, places=2, msg="VIP customer discount not applied correctly.") #Using assertAlmostEqual in case of some rounding errors

    def test_premium_customer_discount(self):
        self.customer = Customer("Samuel Harwood", CustomerType.PREMIUM)
        cart = ShoppingCart(self.customer, DiscountService()) #These need to be defined locally, as in setup the customer is just a regular customer
        cart.add_item(CartItem(self.product_one, 1)) #One laptop
        discount = DiscountService()

        total = discount.apply_discount(total=cart.calculate_total(),customer_type=self.customer.get_customer_type(),cart_items=cart.get_items(),coupon_code="")
        expected_total = cart.calculate_total() * 0.95 #Before discount + 5% off
        #This fails as a 20% discount is being added due to its price being below £10,000. Technically, the 5% is being added correctly, but the test still fails
        self.assertAlmostEqual(total, expected_total, places=2, msg="Premium customer discount not applied correctly.") 

    #Slightly different issue, the customer discount for VIP has a logic error with !=
    def test_vip_customer_discount(self):
        self.customer = Customer("Samuel Harwood", CustomerType.VIP)
        cart = ShoppingCart(self.customer, DiscountService()) 
        cart.add_item(CartItem(self.product_one, 1)) #One laptop
        discount = DiscountService()

        total = discount.apply_discount(total=cart.calculate_total(),customer_type=self.customer.get_customer_type(),cart_items=cart.get_items(),coupon_code="")
        expected_total = cart.calculate_total() * 0.90 #Before discount + 10% off
        self.assertAlmostEqual(total, expected_total, places=2, msg="VIP customer discount not applied correctly.") 

#6. The system shall allow users to enter coupon codes, which can provide additional percentage-based or fixed-amount discounts (10% off with code "DISCOUNT10" or £50 off with code "SAVE50"). 
# Only one coupon code can be applied and the £50 off will be applied before any percentage discounts.
    def test_coupon_code_discount_10(self):
        discount = DiscountService()
        cart = ShoppingCart(self.customer, discount) 
        cart.add_item(CartItem(self.product_one, 1))

        total = discount.apply_discount(total=cart.calculate_total(),customer_type=self.customer.get_customer_type(),cart_items=cart.get_items(),coupon_code="DISCOUNT10")
        expected_total = cart.calculate_total() * 0.9
        self.assertAlmostEqual(total, expected_total, places=2, msg="Price not proportional to discount") 

    def test_coupon_code_save_50(self):
        discount = DiscountService()
        cart = ShoppingCart(self.customer, discount) 
        cart.add_item(CartItem(self.product_one, 1))

        total = discount.apply_discount(total=cart.calculate_total(),customer_type=self.customer.get_customer_type(),cart_items=cart.get_items(),coupon_code="SAVE50") #Use save50 discount
        expected_total = cart.calculate_total() - 50 #Should just be -50, no over discount should take place
        self.assertEqual(total, expected_total, msg="Price not proportional to discount") 

    #This test should cause a value error, as it is discounting to a negative numbver
    def test_coupon_code_save_50_fail(self):
        discount = DiscountService()
        cart = ShoppingCart(self.customer, discount) 
        cheap_product = Product("PEZ dispenser", 10.00, 10) #It costs less than promotion takes off the price
        cart.add_item(CartItem(cheap_product, 1))
        #To solve this, a check should take place to make sure the carts total is above a certain threshold before adding discounts
        #I think a value error would make the most sense, which is why I added it below
        with self.assertRaises(ValueError, msg="Applying a discount to reduce the price below zero should raise ValueError"):
            discount.apply_discount(total=cart.calculate_total(),customer_type=self.customer.get_customer_type(),cart_items=cart.get_items(),coupon_code="SAVE50") #Use save50 discount


#7. The system shall support time-limited promotions that can be activated or deactivated to apply a flat discount (25% off during a promotional event). 
    def test_time_limited_promotions(self):
        #Ive found that the mocks of discount service in setup really effect the assertions of this and the above tests
        #Which is why all of them have the service referenced locally
        discount = DiscountService()
        cart = ShoppingCart(self.customer, discount)
        cart.add_item(CartItem(self.product_one, 1))
        cart.set_promotion_active(True)

        final_price = cart.calculate_final_price()
        expected_price = cart.calculate_total() * 0.75  
        #I am surprused this one actually works!
        self.assertAlmostEqual(final_price, expected_price, places=2, msg="Promotion discount should be 25% off base price")

#8. The discounts listed in points 3 to 7 are applied on top of each other in the order they have been specified. 
    def test_apply_multiple_discounts(self):
        self.customer = Customer("Samuel HArwood", CustomerType.VIP)  # VIP customer
        self.cart = ShoppingCart(self.customer, DiscountService())
        self.cart.add_item(CartItem(self.product_one, 1))  # 1 Laptop
        self.cart.add_item(CartItem(self.product_two, 1))  # 1 Mouse
        
        self.cart.apply_coupon_code("DISCOUNT10")  # 10% off with coupon code
        self.cart.set_promotion_active(True)

        total_before_discounts = self.cart.calculate_total()  # Should be 1025.00

        # Calculate the expected final price step by step
        mouse_discount = self.product_two.get_price() * 0.05  # 5% off Mouse price
        total_after_mouse_discount = total_before_discounts - mouse_discount  # Apply mouse discount

        vip_discount = total_after_mouse_discount * 0.90  # 10% off
        coupon_discount = vip_discount * 0.90  # Additional 10% off for coupon
        expected_final_price = coupon_discount * 0.75  # Another 25% off for the promotion

        total_after_all_discounts = self.cart.calculate_final_price() #10% coupon, %5 off mouse, %10 VIP, 

        self.assertAlmostEqual(total_after_all_discounts, expected_final_price, places=2, msg="The cumulative discounts were not applied correctly.")
        #This test was obviously never going to work as theres no implementation to ensure these stack correctly. 
        #Its about £150 out, so with the logic corrected, might actually return True

#9. The system shall print a detailed receipt summarizing the items in the cart, the total price before discounts, and the final price after all applicable discounts. 
