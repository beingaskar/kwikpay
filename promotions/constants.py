from django.utils.translation import ugettext_lazy as _


COUPON_DRAFT = 'draft'
COUPON_ACTIVE = 'active'
COUPON_INACTIVE = 'inactive'

MULTI_USE = 'multi_use'
ONCE_PER_ACCOUNT = 'once_per_account'
FIRST_RECHARGE_ONLY = 'first_recharge'

COUPON_STATUSES = (
    (COUPON_DRAFT, _('Draft')),
    (COUPON_ACTIVE, _('Active')),
    (COUPON_INACTIVE, _('Inactive'))
)

USAGE_CHOICES = (
    (ONCE_PER_ACCOUNT, _("Can only be used once per account")),
    (FIRST_RECHARGE_ONLY, _("Can only be used during first recharge.")),
    (MULTI_USE, _("Can be used multiple times by multiple account")),
)

DISCOUNT_TYPE_FIXED = 'fixed'
DISCOUNT_TYPE_PERCENTAGE = 'percentage'

DISCOUNT_TYPES = (
    (DISCOUNT_TYPE_FIXED, _('Fixed')),
    (DISCOUNT_TYPE_PERCENTAGE, _('Percentage'))
)
