from django.contrib import admin
from .models import Merchant, Ledger, Payout

admin.site.register(Merchant)
admin.site.register(Ledger)
admin.site.register(Payout)