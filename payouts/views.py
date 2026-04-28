from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .models import Merchant, Ledger, Payout
import json


def balance(request, merchant_id):
    merchant = Merchant.objects.get(id=merchant_id)

    total = 0
    entries = Ledger.objects.filter(merchant=merchant)

    for i in entries:
        if i.entry_type == "credit":
            total += i.amount_paise
        elif i.entry_type == "debit":
            total -= i.amount_paise
        elif i.entry_type == "hold":
            total -= i.amount_paise
        elif i.entry_type == "release":
            total += i.amount_paise

    return JsonResponse({
        "merchant": merchant.name,
        "balance_paise": total
    })


@csrf_exempt
def payout_request(request, merchant_id):
    if request.method == "POST":

        with transaction.atomic():

            merchant = Merchant.objects.select_for_update().get(id=merchant_id)

            key = request.headers.get("Idempotency-Key")

            if key:
                old = Payout.objects.filter(
                    merchant=merchant,
                    idempotency_key=key
                ).first()

                if old:
                    return JsonResponse({
                        "message": "Already exists",
                        "payout_id": old.id,
                        "status": old.status
                    })

            data = json.loads(request.body)

            amount = int(data["amount_paise"])
            bank = data["bank_account_id"]

            total = 0
            entries = Ledger.objects.filter(merchant=merchant)

            for i in entries:
                if i.entry_type == "credit":
                    total += i.amount_paise
                elif i.entry_type == "debit":
                    total -= i.amount_paise
                elif i.entry_type == "hold":
                    total -= i.amount_paise
                elif i.entry_type == "release":
                    total += i.amount_paise

            if total < amount:
                return JsonResponse({
                    "error": "Insufficient balance"
                })

            p = Payout.objects.create(
                merchant=merchant,
                amount_paise=amount,
                bank_account_id=bank,
                idempotency_key=key,
                status="pending"
            )

            Ledger.objects.create(
                merchant=merchant,
                entry_type="hold",
                amount_paise=amount
            )

            return JsonResponse({
                "message": "Payout created",
                "payout_id": p.id
            })