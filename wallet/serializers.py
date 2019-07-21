from django.utils import timezone
from django.db.models import Q
from rest_framework import serializers

from .models import Wallet, AppliedPromotion, Transaction


class AppliedPromotionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppliedPromotion
        fields = ('amount', 'valid_before')


class WalletDetailSerializer(serializers.ModelSerializer):

    promotions = serializers.SerializerMethodField()

    class Meta:
        model = Wallet
        fields = ('id', 'name', 'balance', 'promotions')

    def get_promotions(self, wallet):
        return AppliedPromotionSerializer(
            wallet.appliedpromotion_set.filter(
                Q(valid_before__gte=timezone.now()) |
                Q(valid_before__isnull=True)
            ), many=True).data


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('id', 'amount', 'running_balance', 'timestamp_created')


class PassbookSerializer(serializers.ModelSerializer):

    promotions = serializers.SerializerMethodField()
    recent_transactions = serializers.SerializerMethodField()

    class Meta:
        model = Wallet
        fields = ('name', 'balance', 'promotions', 'recent_transactions')

    def get_promotions(self, wallet):
        return AppliedPromotionSerializer(
            wallet.appliedpromotion_set.filter(
                valid_before__gte=timezone.now()
            ), many=True).data

    def get_recent_transactions(self, wallet):
        return TransactionSerializer(
            wallet.transaction_set.order_by('-timestamp_created')[:10],
            many=True
        ).data

