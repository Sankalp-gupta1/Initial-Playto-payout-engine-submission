from django.core.management.base import BaseCommand
from payouts.models import Payout, Ledger
import random


class Command(BaseCommand):
    help = "Process pending payouts"

    def handle(self, *args, **kwargs):

        payouts = Payout.objects.filter(status="pending")

        for p in payouts:

            chance = random.randint(1, 100)

            if chance <= 70:
                # success
                p.status = "completed"
                p.save()

                Ledger.objects.create(
                    merchant=p.merchant,
                    entry_type="debit",
                    amount_paise=p.amount_paise
                )

                self.stdout.write(
                    f"Payout {p.id} completed"
                )

            else:
                # fail
                p.status = "failed"
                p.save()

                Ledger.objects.create(
                    merchant=p.merchant,
                    entry_type="release",
                    amount_paise=p.amount_paise
                )

                self.stdout.write(
                    f"Payout {p.id} failed"
                )