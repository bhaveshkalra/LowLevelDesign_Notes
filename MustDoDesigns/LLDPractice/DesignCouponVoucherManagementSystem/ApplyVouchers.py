"""
Design a coupon and voucher managment system's Low level design. 
Requirements were: Admin will create coupons with rules(like match age > 18 and cart_value > 1000); 
Coupons will have (averall uses limit / per ser limit ), expiry date , active/inactive etc. 
Vouchers will be of type Unassigned : anyone can use but only one uses "PreAssigned": Voucher attached to user id 
Was asked to  design api too: User will see list of coupons available and Vouchers; Admin can delete/ create , 
activate or disable coupons etc.
"""

"""Requirements
Functional
Admin:
Create / update / delete coupons
Activate / deactivate

User:
View available coupons & vouchers
Apply coupon/voucher

Voucher types:
Unassigned → one-time use globally
PreAssigned → tied to userId

Coupon Rules
Conditions like:
age > 18
cart_value > 1000
Limits:
Global usage limit
Per-user limit
Expiry + active flag
"""

class Coupon:
    def __init__(self, coupon_id, rules, expiry, max_uses, per_user_limit):
        self.coupon_id = coupon_id
        self.rules = rules  # list of Rule objects
        self.expiry = expiry
        self.max_uses = max_uses
        self.per_user_limit = per_user_limit
        self.active = True
        self.total_used = 0

class Voucher:
    def __init__(self, code, voucher_type, assigned_user=None):
        self.code = code
        self.voucher_type = voucher_type  # UNASSIGNED / PREASSIGNED
        self.assigned_user = assigned_user
        self.used = False

class User:
    def __init__(self, user_id, age):
        self.user_id = user_id
        self.age = age
        self.used_coupons = {}  # coupon_id -> count

class Cart:
    def __init__(self, value):
        self.value = value


#Rule Engine->(Strategy Pattern)
class Rule:
    def validate(self, user, cart):
        pass

class AgeRule(Rule):
    def __init__(self, min_age):
        self.min_age = min_age

    def validate(self, user, cart):
        return user.age > self.min_age

class CartValueRule(Rule):
    def __init__(self, min_value):
        self.min_value = min_value

    def validate(self, user, cart):
        return cart.value > self.min_value


class CouponService:
    def __init__(self):
        self.coupons = {}  # coupon_id -> Coupon

    def add_coupon(self, coupon):
        self.coupons[coupon.coupon_id] = coupon

    def delete_coupon(self, coupon_id):
        if coupon_id in self.coupons:
            del self.coupons[coupon_id]

    def activate_coupon(self, coupon_id):
        self.coupons[coupon_id].active = True

    def deactivate_coupon(self, coupon_id):
        self.coupons[coupon_id].active = False

    def get_available_coupons(self, user, cart):
        return [c for c in self.coupons.values()
            if self.validate_coupon(c, user, cart)
        ]

    def validate_coupon(self, coupon, user, cart):
        if not coupon.active:
            return False

        if coupon.total_used >= coupon.max_uses:
            return False

        if user.used_coupons.get(coupon.coupon_id, 0) >= coupon.per_user_limit:
            return False

        # Rule validation
        for rule in coupon.rules:
            if not rule.validate(user, cart):
                return False
        return True

    def apply_coupon(self, coupon, user, cart):
        if not self.validate_coupon(coupon, user, cart):
            raise Exception("Coupon invalid")

        coupon.total_used += 1
        user.used_coupons[coupon.coupon_id] = user.used_coupons.get(coupon.coupon_id, 0) + 1

        return "Discount applied"


class VoucherService:
    def __init__(self):
        self.vouchers = {}  # code -> Voucher

    def add_voucher(self, voucher):
        self.vouchers[voucher.code] = voucher

    def get_vouchers_for_user(self, user):
        result = []
        for v in self.vouchers.values():
            if v.used:
                continue
            if v.voucher_type == "UNASSIGNED":
                result.append(v)
            elif v.voucher_type == "PREASSIGNED" and v.assigned_user == user.user_id:
                result.append(v)
        return result

    def apply_voucher(self, voucher, user):
        if voucher.used:
            raise Exception("Already used")

        if voucher.voucher_type == "PREASSIGNED":
            if voucher.assigned_user != user.user_id:
                raise Exception("Not valid for this user")

        voucher.used = True
        return "Voucher applied"

class Admin:
    def __init__(self, admin_id):
        self.admin_id = admin_id
    def create_coupon(self, coupon_service, coupon):
        coupon_service.add_coupon(coupon)
    def delete_coupon(self, coupon_service, coupon_id):
        coupon_service.delete_coupon(coupon_id)
    def activate_coupon(self, coupon_service, coupon_id):
        coupon_service.activate_coupon(coupon_id)
    def deactivate_coupon(self, coupon_service, coupon_id):
        coupon_service.deactivate_coupon(coupon_id)
    def create_voucher(self, voucher_service, voucher):
        voucher_service.add_voucher(voucher)


class CouponVoucherSystem:
    def __init__(self):
        self.coupon_service = CouponService()
        self.voucher_service = VoucherService()

    # -------- USER APIs --------
    def get_coupons(self, user, cart):
        return self.coupon_service.get_available_coupons(user, cart)

    def get_vouchers(self, user):
        return self.voucher_service.get_vouchers_for_user(user)

    def apply_coupon(self, coupon_id, user, cart):
        coupon = self.coupon_service.coupons.get(coupon_id)
        return self.coupon_service.apply_coupon(coupon, user, cart)

    def apply_voucher(self, code, user):
        voucher = self.voucher_service.vouchers.get(code)
        return self.voucher_service.apply_voucher(voucher, user)

    # -------- ADMIN APIs --------
    def create_coupon(self, coupon):
        self.coupon_service.add_coupon(coupon)

    def delete_coupon(self, coupon_id):
        self.coupon_service.delete_coupon(coupon_id)

    def activate_coupon(self, coupon_id):
        self.coupon_service.activate_coupon(coupon_id)

    def deactivate_coupon(self, coupon_id):
        self.coupon_service.deactivate_coupon(coupon_id)

    def create_voucher(self, voucher):
        self.voucher_service.add_voucher(voucher)

#concurrency handled via DB atomic counters / Redis locks