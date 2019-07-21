from django.urls import path

from .views import ListAccounts


urlpatterns = [

    # List accounts.
    path('', ListAccounts.as_view(), name='list-accounts'),

]
