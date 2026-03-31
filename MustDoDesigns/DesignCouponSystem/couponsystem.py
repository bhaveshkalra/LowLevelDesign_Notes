"""
Design a system to offer coupons to users based on their orders placing on a shopping platform. 
Coupons provided can be like fast one day delivery service as coupon, two day delivery, or normal delivery with off on next order placed & other coupons are 
like providing membership or external websites or platform coupons, so design such a system considering that coupons 
providing is based on or depends on the users ordering personality and no. of orders placed by the user.
"""

"""
Problem:
We need to:
Generate coupons dynamically on new orders
Based on:
User behavior (order frequency, spend, categories)
Number of orders

Support multiple coupon types:
1.Fast delivery (1-day / 2-day)
2.Discount on next order
3.Membership / subscription
4.External platform coupons (partners)


Design:
Strategy Pattern  → Different coupon generators
Factory Pattern   → Choose generator
Rule Engine       → Decide eligibility
Coupon Manager    → Orchestrator
"""

from enum import Enum
from datetime import datetime, timedelta
from abc import ABC, abstractmethod


class CouponType(Enum):
    DELIVERY = "delivery"
    DISCOUNT = "discount"
    MEMBERSHIP = "membership"
    EXTERNAL = "external"


class User:
    def __init__(self, user_id : str):
        self.user_id = user_id
        self.orders = [] #list of orders placed by the user
        self.active_member = False #membership status

    def total_orders(self):
        return len(self.orders)
    
    def total_spent(self):
        return sum(order.amount for order in self.orders)


class Order:
    def __init__(self, order_id : str, amount : float, order_date = None):
        self.order_id = order_id
        self.amount = amount
        self.order_date = order_date or datetime.now()


class Coupon:
    def __init__(self, coupon_id, coupon_type: CouponType, description, expiry):
        self.coupon_id = coupon_id
        self.coupon_type = coupon_type
        self.description = description
        self.expiry = expiry

    def is_valid(self):
        return datetime.now() < self.expiry

    def __repr__(self):
        return f"<Coupon {self.coupon_type.value}: {self.description}>"
    


class UserProfile:
    def __init__(self, user: User):
        self.user = user

    def is_frequent_buyer(self):
        return self.user.total_orders() > 10

    def is_high_spender(self):
        return self.user.total_spent() > 5000

    def is_new_user(self):
        return self.user.total_orders() < 3

    def is_inactive(self):
        if not self.user.orders:
            return True
        last_order = max(o.order_date for o in self.user.orders)
        return (datetime.now() - last_order).days > 30


class CouponStrategy(ABC): #interface, strategry pattern for different coupon generation strategies based on rules
    @abstractmethod
    def is_applicable(self, profile):
        pass

    @abstractmethod
    def generate(self, profile):
        pass

    @abstractmethod
    def score(self, profile):
        pass


class DeliveryCouponStrategy(CouponStrategy):
    def is_applicable(self, profile):
        return profile.is_frequent_buyer()

    def generate(self, user_profile):
        return Coupon(
            "DEL-1DAY",
            CouponType.DELIVERY,
            "Free 1-day delivery",
            datetime.now() + timedelta(days=5))
    def score(self, profile):
        return 70  #medium priority


class DiscountCouponStrategy(CouponStrategy):
    def is_applicable(self, profile):
        return profile.is_inactive()

    def generate(self, user_profile):
        return Coupon(
            "DISC-100",
            CouponType.DISCOUNT,
            "Flat ₹100 off on next order",
            datetime.now() + timedelta(days=7))
    def score(self, profile):
        return 90  #high priority 


class MembershipCouponStrategy(CouponStrategy):
    def is_applicable(self, profile):
        return profile.is_high_spender() and not profile.user.membership_active

    def generate(self, user_profile):
        return Coupon(
            "FREE-MEMBERSHIP",
            CouponType.MEMBERSHIP,
            "1 month free membership",
            datetime.now() + timedelta(days=10))

    def score(self, profile):
        return 60 #Low priority


class ExternalCouponStrategy(CouponStrategy):#uber, zomato, swiggy etc
    def is_applicable(self, profile):
        return user_profile.is_new_user()

    def generate(self, user_profile):
        return Coupon(
            "EXT-ZOMATO",
            CouponType.EXTERNAL,
            "Free ZOMATO coupon",
            datetime.now() + timedelta(days=3))
    def score(self, profile):
        return 80 #Medium priority


class CouponStrategyFactory:
    def get_strategies(self):
        return [
            DeliveryCouponStrategy(),
            DiscountCouponStrategy(),
            MembershipCouponStrategy(),
            ExternalCouponStrategy()
        ]


class CouponSelector:
    def select_best(self, strategies, profile):
        best_coupon = None
        best_score = -1
        for strategy in strategies:
            if not strategy.is_applicable(profile):
                continue

            score = strategy.score(profile)
            if score > best_score:
                best_score = score
                best_coupon = strategy.generate(profile)
        return best_coupon


class CouponEngine:
    def __init__(self):
        self.factory = CouponStrategyFactory()
        self.selector = CouponSelector()

    def generate_coupon_for_next_order(self, user: User):
        profile = UserProfile(user)

        strategies = self.factory.get_strategies()
        coupon = self.selector.select_best(strategies, profile)
        return coupon


if __name__ == "__main__":
    user = User("U1")

    #old orders
    for i in range(12):
        user.orders.append(Order(f"O{i}", amount=500))

    engine = CouponEngine()
    coupon = engine.generate_coupon_for_next_order(user)

    print("Selected coupon:", coupon)

