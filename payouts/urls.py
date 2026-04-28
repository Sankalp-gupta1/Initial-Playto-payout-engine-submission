from django.urls import path
from .views import balance, payout_request

urlpatterns = [
    path("balance/<int:merchant_id>/", balance),
    path("payout/<int:merchant_id>/", payout_request),
]