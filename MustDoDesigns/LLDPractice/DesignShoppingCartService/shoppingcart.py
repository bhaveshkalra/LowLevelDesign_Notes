"""
Write code that will be used by a Shopping cart service to enforce rules on the order
eg. Offer free 2 day shipping on orders > $35 if customer is not a prime member
Offer free 2 day shipping on all orders if customer is a prime member
Offer free 1 day shipping for order that are > $125
Offer free 2 hour shipping for prime customer that have > $25 and the items are grocery items
Make this extensible to add other rules in the future
Apply a 10 % discount if an item has been marked for subscribe and save.
"""
#Chain of responsbility pattern is used here to make the system extensible and maintainable. 
#Each handler in the chain is responsible for checking a specific rule and applying it if the conditions are met. 
#If a handler cannot handle the request, it passes it to the next handler in the chain. 
#This allows for easy addition of new rules in the future without modifying existing code, 
#adhering to the Open/Closed Principle of software design.

from abc import ABC, abstractmethod

class Cart:
    def __init__(self, prime_member, items):
        self.prime_member = prime_member
        self.items = items
        self.shipping_cost = None
        self.shipping_type = None
        self.total_amount = sum(item.price for item in items)

    def is_grocery_only(self):
        return all(item.is_grocery for item in self.items)

class Item:
    def __init__(self, name, price, subscribe_and_save=False, is_grocery=False):
        self.name = name
        self.price = price
        self.subscribe_and_save = subscribe_and_save
        self.is_grocery = is_grocery

class Handler(ABC):
    def __init__(self):
        self._next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, cart):
        if self._next_handler:
            return self._next_handler.handle(cart)

class FreeShippingHandler(Handler):
    def handle(self, cart):
        if cart.prime_member or cart.total_amount > 35:
            cart.shipping_cost = 0
            cart.shipping_type = '2 day'
        return super().handle(cart)

class OneDayShippingHandler(Handler):
    def handle(self, cart):
        if cart.total_amount > 125:
            cart.shipping_cost = 0
            cart.shipping_type = '1 day'
        return super().handle(cart)

class TwoHourShippingHandler(Handler):
    def handle(self, cart):
        if cart.prime_member and cart.total_amount > 25 and cart.is_grocery_only():
            cart.shipping_cost = 0
            cart.shipping_type = '2 hour'
        return super().handle(cart)

class DiscountHandler(Handler):
    def handle(self, cart):
        for item in cart.items:
            if item.subscribe_and_save:
                item.price *= 0.9  # Apply 10% discount
        # Recalculate total amount after discounts
        cart.total_amount = sum(item.price for item in cart.items)
        return super().handle(cart)

# Example usage
items = [
    Item('Milk', 3.5, subscribe_and_save=True, is_grocery=True),
    Item('Bread', 2.5, is_grocery=True),
]
cart = Cart(prime_member=True, items=items)

# Create handlers
free_shipping_handler = FreeShippingHandler()
one_day_shipping_handler = OneDayShippingHandler()
two_hour_shipping_handler = TwoHourShippingHandler()
discount_handler = DiscountHandler()

# Chain the handlers
free_shipping_handler.set_next(one_day_shipping_handler).set_next(two_hour_shipping_handler).set_next(discount_handler)

# Start the chain
free_shipping_handler.handle(cart)