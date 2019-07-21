from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import exceptions
from django.conf import settings
from django.db import transaction

from base.serializers import PaginatedSerializer
from base.renderers import custom_response_renderer
from wallet.models import Transaction
from promotions.helper import PromotionHelper
from .serializers import WalletDetailSerializer, PassbookSerializer, \
    TransactionSerializer

API_PAGE_COUNT_DEFAULT = getattr(settings, 'API_PAGE_COUNT_DEFAULT', 25)
API_PAGE_COUNT_MAX = getattr(settings, 'API_PAGE_COUNT_MAX', 25)


class CheckBalance(APIView):
    """ API to get wallet balance of logged-in user.
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = WalletDetailSerializer

    def post(self, request):

        wallet = request.user.get_wallet()

        data = {}

        if wallet:
            data = self.serializer_class(wallet).data

        return custom_response_renderer(
            data=data, status=True, status_code=status.HTTP_200_OK)


class DepositAmount(APIView):
    """ API to deposit an amount to user's wallet.
    """

    permission_classes = (IsAuthenticated, )

    def post(self, request):

        amount = request.data.get('amount', None)
        promo_code = request.data.get('promo', None)

        success, error_msg, data = True, None, {}

        if (not amount) or (amount <= 0):
            success = False
            error_msg = "Invalid amount."

        promo_value = None
        if promo_code:
            promo_value = PromotionHelper(
                request.user).calculate_discount(promo_code, amount)
            if not promo_value or not promo_value['status']:
                success = False
                error_msg = "Invalid promo code."

        if success:
            wallet = request.user.get_wallet()

            if not wallet:
                success = False
                error_msg = "Wallet does not exist for user."

        if success:
            with transaction.atomic():
                wallet.deposit(amount)
                if promo_value:
                    wallet.apply_promo(
                        promo_value['promo_id'], promo_value['amount'],
                        promo_value['validity_val'],
                        promo_value['validity_unit']
                    )
            data = WalletDetailSerializer(wallet).data

        return custom_response_renderer(
            data=data,
            error_msg=error_msg,
            status=success,
            status_code=status.HTTP_200_OK if success else
            status.HTTP_400_BAD_REQUEST
        )


class WithdrawAmount(APIView):
    """ API to withdraw amount from user's wallet.
    """

    permission_classes = (IsAuthenticated, )

    def post(self, request):

        amount = request.data.get('amount', None)

        success, error_msg, data = True, None, {}

        if (not amount) or (amount <= 0):
            success = False
            error_msg = "Invalid amount."
        if success:
            wallet = request.user.get_wallet()

            if not wallet:
                success = False
                error_msg = "Wallet does not exist for user."

        if success:
            wallet.withdraw(amount)
            data = WalletDetailSerializer(wallet).data

        return custom_response_renderer(
            data=data,
            error_msg=error_msg,
            status=success,
            status_code=status.HTTP_200_OK if success else
            status.HTTP_400_BAD_REQUEST
        )


class GetMiniStatement(APIView):
    """ API to get mini-statement of logged-in user's wallet.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = PassbookSerializer

    def post(self, request):
        wallet = request.user.get_wallet()

        data = {}

        if wallet:
            data = self.serializer_class(wallet).data

        return custom_response_renderer(
            data=data, status=True, status_code=status.HTTP_200_OK)


class ListTransactions(APIView):
    """ API to list all money transactions.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer

    def post(self, request, pk):
        if request.user.is_staff:
            transactions = Transaction.objects.filter(
                wallet_id=pk).order_by('-timestamp_created')
        else:
            wallet = request.user.get_wallet()
            if not wallet:
                raise exceptions.APIException(
                    "Wallet not found.")
            if wallet.id != pk:
                raise exceptions.PermissionDenied()

            transactions = wallet.transaction_set.order_by(
                '-timestamp_created')

        count = int(request.GET.get('count', API_PAGE_COUNT_DEFAULT))
        page = int(request.GET.get('page', 1))

        data = PaginatedSerializer(
            queryset=transactions,
            num=min(count, API_PAGE_COUNT_MAX),
            page=page,
            serializer_method=self.serializer_class
        ).data

        return custom_response_renderer(
            data=data, status=True, status_code=status.HTTP_200_OK)
