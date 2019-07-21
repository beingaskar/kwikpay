from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import transaction, IntegrityError

from base.models import BaseModel
from base.helper import TimeHelper
from promotions.models import PromotionRule


class Wallet(BaseModel):
    """ Wallet model. Stores wallet related details.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
        related_name='wallet'
    )

    name = models.CharField(
        _('Name'), max_length=255, unique=True, default='default',
        help_text=_('Name of the Wallet')
    )

    balance = models.DecimalField(
        _('Wallet Balance'), max_digits=10, decimal_places=2, default=0
    )

    @transaction.atomic
    def deposit(self, amount):
        """ Deposit `amount` to wallet.
        """

        amount = Decimal(amount)

        self.transaction_set.create(
            amount=amount,
            running_balance=self.balance + amount
        )
        self.balance += amount
        self.save()

    @transaction.atomic
    def withdraw(self, amount):
        """ Withdraw `amount` to wallet.
        """

        amount = Decimal(amount)

        if amount > self.balance:
            raise IntegrityError("Insufficient Balance")

        self.transaction_set.create(
            amount=-amount,
            running_balance=self.balance - amount
        )
        self.balance -= amount
        self.save()

    @transaction.atomic
    def apply_promo(
            self, rule_id, amount, validity_val=None, validity_unit=None):

        valid_till = None

        if validity_val and validity_unit:
            valid_till = TimeHelper.calculate_future_time(
                validity_val, validity_unit)
        self.appliedpromotion_set.create(
            promotion_rule_id=rule_id,
            amount=amount,
            valid_before=valid_till
        )

    class Meta:
        unique_together = [['user', 'name']]

    def __str__(self):
        return self.name


class Transaction(BaseModel):
    """ `Transaction` model to store any money transaction details.
    """

    wallet = models.ForeignKey(
        Wallet, null=True, on_delete=models.SET_NULL
    )

    amount = models.DecimalField(
        _('Amount'), max_digits=10, decimal_places=2, default=0
    )

    running_balance = models.DecimalField(
        _('Wallet Balance at the time of transaction'), max_digits=10,
        decimal_places=2, default=0
    )

    def __str__(self):
        return self.wallet.name


class AppliedPromotion(BaseModel):
    """ `Applied Promotion` model to store promotion details applied on
    any wallet.
    """

    wallet = models.ForeignKey(
        Wallet, null=True, on_delete=models.SET_NULL
    )

    promotion_rule = models.ForeignKey(
        PromotionRule, null=True, on_delete=models.SET_NULL
    )

    amount = models.DecimalField(
        _('Amount'), max_digits=10, decimal_places=2, default=0
    )

    valid_before = models.DateTimeField(
        _('Valid until'), null=True, blank=True
    )

    def __str__(self):
        return self.wallet.user.email

