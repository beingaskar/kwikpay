from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django_fsm import FSMField, transition

from base.models import BaseModel

from .constants import COUPON_STATUSES, COUPON_ACTIVE, DISCOUNT_TYPES, \
    DISCOUNT_TYPE_PERCENTAGE, USAGE_CHOICES, ONCE_PER_ACCOUNT, COUPON_INACTIVE


class PromotionRule(BaseModel):
    """ PromotionRule model. Any coupon should be declared here along with
    any conditions.
    """

    code = models.CharField(
        _('Promo Code'), max_length=128, unique=True,
        help_text=_('Promo Code')
    )

    valid_from = models.DateTimeField(_('Valid from'))

    valid_till = models.DateTimeField(_('Valid till'))

    status = FSMField(
        _('Status'), max_length=128, choices=COUPON_STATUSES,
        default=COUPON_ACTIVE,
    )

    # Fields related to applying Logic

    discount_type = models.CharField(
        _('Discount Type'), max_length=128, choices=DISCOUNT_TYPES,
        default=DISCOUNT_TYPE_PERCENTAGE,
    )

    discount_value = models.DecimalField(
        _('Discount Value'), max_digits=10, decimal_places=2, default=0
    )

    discount_max = models.DecimalField(
        _('Maximum discount allowed'), max_digits=6, decimal_places=2,
        default=0, null=True, blank=True,
        help_text=_(
            'Max. cap for discount for coupon (applicable if discount_type is '
            'percentage)')
    )

    validity_days = models.PositiveIntegerField(
        _('Promo balance validity in days'), null=True, blank=True,
        help_text=_('Number of days for which promo balance is valid.')
    )

    # Fields related to conditions.

    usage_type = models.CharField(
        _('Usage Type (Account level)'), max_length=128, choices=USAGE_CHOICES,
        default=ONCE_PER_ACCOUNT
    )

    usage_limit_overall = models.PositiveIntegerField(
        _('Maximum number of redemption.'), null=True, blank=True,
        help_text=_('Max. number of times coupon can be used')
    )

    usage_limit_account = models.PositiveIntegerField(
        _('Limit per Account'), null=True, blank=True,
        help_text=_('Max. number of times coupon can be used per account.')
    )

    recharge_minimum = models.PositiveIntegerField(
        _('Minimum recharge required.'), null=True, blank=True,
        help_text=_('Minimum recharge required to apply promo code.')
    )

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        now = timezone.now()
        if PromotionRule.objects.filter(
                code=self.code, status=COUPON_ACTIVE, valid_from__lte=now,
                valid_till__gt=now).exclude(id=self.id).exists():
            raise ValidationError(_('Promo code already exists.'))
        else:
            super(PromotionRule, self).save(*args, **kwargs)

    # Transition Conditions

    def can_be_activated(self):
        now = timezone.now()
        return (self.valid_from < now) and (self.valid_till > now)

    @transition(field=status, source=[COUPON_ACTIVE], target=COUPON_INACTIVE,
                conditions=[])
    def deactivate(self):
        pass

    @transition(field=status, source=[COUPON_INACTIVE], target=COUPON_ACTIVE,
                conditions=[can_be_activated])
    def activate(self):
        pass
