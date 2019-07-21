from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from base.renderers import custom_response_renderer
from promotions.helper import PromotionHelper


class ValidatePromoCode(APIView):
    """ Validates the promo code for the user.
    """

    permission_classes = (IsAuthenticated, )

    def post(self, request):

        promo_code = request.data.get('promo', None)
        amount = request.data.get('amount', None)

        if promo_code and amount:
            data = PromotionHelper(
                request.user).calculate_discount(
                promo_code, amount, request.user.get_wallet())
            error_msg = None
            is_success = data['status']
        else:
            data = None
            error_msg = "Insufficient arguments."
            is_success = False

        return custom_response_renderer(
            data=data,
            error_msg=error_msg,
            status=is_success,
            status_code=status.HTTP_200_OK
        )
