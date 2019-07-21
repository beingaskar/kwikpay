from django.contrib import admin

from base.admin import NonEditableAdmin, NonEditableTabularInlineAdmin

from .models import Wallet, Transaction, AppliedPromotion


@admin.register(AppliedPromotion)
class AppliedPromotionAdmin(NonEditableAdmin):
    list_display = ('id', 'wallet', 'user', 'amount', 'valid_before')

    list_filter = ['promotion_rule', ]

    def user(self, obj):
        return obj.wallet.user

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('wallet', 'wallet__user')
        return qs


class TransactionInline(NonEditableTabularInlineAdmin):
    model = Transaction
    min_num = 0
    extra = 0
    max_num = 100

    fields = ['id', 'timestamp_created', 'amount', 'running_balance']

    readonly_fields = ['timestamp_created']

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-timestamp_created')


@admin.register(Wallet)
class WalletAdmin(NonEditableAdmin):
    list_display = ('id', 'user', 'name', 'balance')

    inlines = [TransactionInline]
