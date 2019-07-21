from django.contrib import admin

from fsm_admin.mixins import FSMTransitionMixin

from .models import PromotionRule
from .constants import COUPON_ACTIVE, COUPON_INACTIVE


@admin.register(PromotionRule)
class PromotionRuleAdmin(FSMTransitionMixin, admin.ModelAdmin):
    """ Customized admin for `PromotionRule` model.
    """

    list_display = (
        'id', 'code', 'valid_from', 'valid_till', 'status',  'discount_type',
        'discount_value', 'discount_max',  'validity_days', 'usage_type',
        'usage_limit_overall', 'usage_limit_account', 'recharge_minimum'
    )

    list_filter = ['status']

    fsm_field = ['status', ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.status in [COUPON_ACTIVE, COUPON_INACTIVE]:
            return False
        return super(PromotionRuleAdmin, self).has_change_permission(
            request, obj=obj)
