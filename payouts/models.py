from django.db import models


class Merchant(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Ledger(models.Model):
    TYPE_CHOICES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
        ('hold', 'Hold'),
        ('release', 'Release'),
    ]

    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    entry_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount_paise = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.entry_type


class Payout(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    amount_paise = models.BigIntegerField()
    bank_account_id = models.CharField(max_length=100)
    idempotency_key = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.status