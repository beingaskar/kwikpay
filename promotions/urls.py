from django.urls import path

from .views import ValidatePromoCode


urlpatterns = [

    # Check if promo-code is valid.
    path('validate/', ValidatePromoCode.as_view(), name='validate-promo-code'),

]
