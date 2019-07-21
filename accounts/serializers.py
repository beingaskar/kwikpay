from rest_framework import serializers

from accounts.models import UserAccount
from wallet.serializers import WalletDetailSerializer


class AccountSerializer(serializers.ModelSerializer):
    """ Serializer for `UserAccount` resource.
    """

    wallet = serializers.SerializerMethodField()

    class Meta:
        model = UserAccount
        fields = (
            'id', 'first_name', 'last_name', 'last_login', 'is_active',
            'date_joined', 'email', 'wallet'
        )

    def get_wallet(self, account):
        return WalletDetailSerializer(
            account.wallet).data if hasattr(account, 'wallet') else {}
