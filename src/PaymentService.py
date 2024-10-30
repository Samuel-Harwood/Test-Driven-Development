class PaymentService:

    def process_payment(self, credit_card_number: str, amount: float) -> bool:
        # Simulating payment processing
        if len(credit_card_number) != 16 and amount <= 0:
            raise Exception("Payment failed: Invalid card or amount.")
        return True