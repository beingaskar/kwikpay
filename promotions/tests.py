from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from wallet.models import Wallet, AppliedPromotion
from promotions.models import PromotionRule
from promotions.helper import PromotionHelper
from promotions.constants import (
    COUPON_ACTIVE, COUPON_INACTIVE, DISCOUNT_TYPE_PERCENTAGE)


class PromotionTests(TransactionTestCase):

    BALANCE_INITIAL = 10000
    RECHARGE_MINIMUM = 3999
    MAX_DISCOUNT = 225
    PROMO_CODE = "XYZ321"
    DISCOUNT_PERCENTAGE=15

    def setUp(self):
        """ Setups the test environment. Creates user and wallet.
        """

        print("Setting up the test environment.")
        self.user = get_user_model()()
        self.user.save()
        print("Created user.")
        self.wallet = Wallet(
            user=self.user, name="default", balance=self.BALANCE_INITIAL)
        self.wallet.save()
        print("Created wallet.")
        self.promo_code = PromotionRule(
            code=self.PROMO_CODE,
            valid_from=timezone.now()-timedelta(days=1),
            valid_till=timezone.now() + timedelta(days=1),
            status=COUPON_ACTIVE,
            discount_type=DISCOUNT_TYPE_PERCENTAGE,
            discount_value=self.DISCOUNT_PERCENTAGE,
            discount_max=self.MAX_DISCOUNT,
            recharge_minimum=self.RECHARGE_MINIMUM
        )
        self.promo_code.save()
        print("Created promotion.")

    def test_validate_promotion_rule(self):

        # Minimum balance validation.
        discount = PromotionHelper(
            self.user).calculate_discount(self.PROMO_CODE, 1000)
        self.assertFalse(discount['status'])
        discount = PromotionHelper(self.user).calculate_discount(
            self.PROMO_CODE, self.RECHARGE_MINIMUM)
        self.assertTrue(discount['status'])

        # Discount value validation.
        self.assertEqual(discount['amount'], self.MAX_DISCOUNT)

    def test_status_handling(self):
        self.assertEqual(self.promo_code.status, COUPON_ACTIVE)
        self.promo_code.deactivate()
        self.assertEqual(self.promo_code.status, COUPON_INACTIVE)
        self.promo_code.activate()
        self.assertEqual(self.promo_code.status, COUPON_ACTIVE)

    def test_wallet_deposit_with_promo(self):
        discount = PromotionHelper(self.user).calculate_discount(
            self.PROMO_CODE, self.RECHARGE_MINIMUM)
        self.assertTrue(discount['status'])

        self.wallet.apply_promo(
            discount['promo_id'],
            discount['amount'],
            discount['validity_val'],
            discount['validity_unit']
        )

        applied_promotion = AppliedPromotion.objects.last()
        self.assertEqual(applied_promotion.wallet, self.wallet)
        self.assertEqual(
            applied_promotion.promotion_rule_id, discount['promo_id'])
        self.assertEqual(applied_promotion.amount, discount['amount'])
        self.assertEqual(applied_promotion.valid_before, None)
