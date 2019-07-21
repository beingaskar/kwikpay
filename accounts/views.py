from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from base.renderers import custom_response_renderer
from base.serializers import PaginatedSerializer
from accounts.models import UserAccount
from accounts.serializers import AccountSerializer

API_PAGE_COUNT_DEFAULT = getattr(settings, 'API_PAGE_COUNT_DEFAULT', 25)
API_PAGE_COUNT_MAX = getattr(settings, 'API_PAGE_COUNT_MAX', 25)


class ListAccounts(APIView):
    """ List all accounts registered under the service.
    Expected to be used by admin user.
    """

    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = AccountSerializer

    def post(self, request):

        count = int(request.GET.get('count', API_PAGE_COUNT_DEFAULT))
        page = int(request.GET.get('page', 1))

        data = PaginatedSerializer(
            queryset=UserAccount.objects.all(),
            num=min(count, API_PAGE_COUNT_MAX),
            page=page,
            serializer_method=self.serializer_class
        ).data

        return custom_response_renderer(
            data=data, status=True, status_code=status.HTTP_200_OK)
