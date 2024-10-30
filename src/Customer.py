from CustomerType import CustomerType


class Customer:
    def __init__(self, name, customer_type: CustomerType):
        if not isinstance(customer_type, CustomerType):
            raise ValueError("customer_type must be an instance of CustomerType")

        self._name = name
        self._customer_type = customer_type

    # Getters
    def get_name(self):
        return self._name

    def get_customer_type(self):
        return self._customer_type

    # Setters
    def set_name(self, name):
        self._name = name

    def set_customer_type(self, customer_type):
        self._customer_type = customer_type
