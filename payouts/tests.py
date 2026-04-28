from django.test import TestCase, Client
from .models import Merchant, Ledger, Payout
import json


class PayoutTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.merchant = Merchant.objects.create(
            name="Test Merchant"
        )

        Ledger.objects.create(
            merchant=self.merchant,
            entry_type="credit",
            amount_paise=100000
        )

    def test_idempotency(self):

        data = {
            "amount_paise": 50000,
            "bank_account_id": "abc"
        }

        h = {"HTTP_IDEMPOTENCY_KEY": "same-key"}

        r1 = self.client.post(
            f"/api/payout/{self.merchant.id}/",
            data=json.dumps(data),
            content_type="application/json",
            **h
        )

        r2 = self.client.post(
            f"/api/payout/{self.merchant.id}/",
            data=json.dumps(data),
            content_type="application/json",
            **h
        )

        self.assertEqual(
            Payout.objects.count(),
            1
        )

    def test_insufficient_balance(self):

        data = {
            "amount_paise": 200000,
            "bank_account_id": "abc"
        }

        r = self.client.post(
            f"/api/payout/{self.merchant.id}/",
            data=json.dumps(data),
            content_type="application/json"
        )

        self.assertContains(
            r,
            "Insufficient"
        )