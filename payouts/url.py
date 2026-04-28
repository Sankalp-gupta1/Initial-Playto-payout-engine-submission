from django.urls import path
from .views import balance

urlpatterns = [
    path("balance/<int:merchant_id>/", balance),
]