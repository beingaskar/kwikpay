from decimal import Decimal
import operator
from functools import reduce
from django.utils import timezone
from django.db.models import Q

from .models import PromotionRule
from wallet.models import AppliedPromotion
from .constants import (
    COUPON_ACTIVE, MULTI_USE, DISCOUNT_TYPE_PERCENTAGE)


class PromotionHelper(object):
    """ Helper class to perform operations on `PromotionRule`s.
    """

    def __init__(self, user):
        self.user = user

    @staticmethod
    def get_display_message(promotion_rule):
        if promotion_rule.discount_type == DISCOUNT_TYPE_PERCENTAGE:
            msg = str(promotion_rule.discount_value) + " % promo applied."
        else:
            msg = str(promotion_rule.discount_value) + " promo applied."
        return msg

    @staticmethod
    def __get_discountable_amount(promotion_rule, amount):
        """ Return discountable amount given `promotion_rule` and `amount`.
        :param promotion_rule: PromotionRule instance
        :param amount: float
        :return: int
        """

        amount = Decimal(amount)
        if promotion_rule.discount_type == DISCOUNT_TYPE_PERCENTAGE:
            value = (promotion_rule.discount_value * amount) / Decimal(100.0)
        else:
            value = promotion_rule.discount_value

        if promotion_rule.discount_max:
            value = min(value, promotion_rule.discount_max)

        return value

    def calculate_discount(self, code, amount):
        """ Return's allowed discount given the `code` and `amount`.
        :param code: str
        :param amount: float
        :return: dict
        """

        result = {
            'status': False,
            'amount': 0.0,
            'validity_val': 0,
            'validity_unit': 'days',
            'message': "",
            'promo_id': None
        }

        now = timezone.now()
        query = [
            Q(code=code),
            Q(valid_from__lte=now),
            Q(valid_till__gt=now),
            Q(status=COUPON_ACTIVE)
        ]

        promotion_rule = PromotionRule.objects.filter(
            reduce(operator.and_, query)
        ).last()

        if promotion_rule:
            result['status'] = True

        if result['status']:
            count_redeemed_user = AppliedPromotion.objects.filter(
                wallet__user=self.user,
                promotion_rule=promotion_rule
            ).count()

            count_redeemed_total = AppliedPromotion.objects.filter(
                promotion_rule=promotion_rule
            ).count()

            if count_redeemed_user > 0:
                query.append(Q(usage_type=MULTI_USE))
                query.append(
                    Q(usage_limit_account=None) |
                    Q(usage_limit_account__gt=count_redeemed_user)
                )

            query.append(
                Q(usage_limit_overall=None) |
                Q(usage_limit_overall__gt=count_redeemed_total)
            )

            query.append(
                Q(recharge_minimum=None) | Q(recharge_minimum__lte=amount)
            )

            promotion_rule = PromotionRule.objects.filter(
                reduce(operator.and_, query)
            ).first()

            if not promotion_rule:
                result['status'] = False
                result['message'] = "Promo code not valid."
            else:
                result['message'] = self.get_display_message(promotion_rule)
                result['amount']= self.__get_discountable_amount(
                    promotion_rule, amount)
                result['validity_val'] = promotion_rule.validity_days
                result['promo_id'] = promotion_rule.id

        return result
