# Playto Payout Engine

Minimal payout engine built using Django.

## Features

- Merchant balance system using ledger entries
- Payout request API
- Idempotency key support
- Concurrency protection using row locking
- Background payout processor
- Automated tests

## Tech Stack

- Django
- SQLite (can switch to PostgreSQL)
- Django ORM

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install django djangorestframework
python manage.py migrate
python manage.py runserver


# EXPLAINER

## 1. Ledger

Balance is calculated using ledger entries:

- credit = money added
- debit = payout completed
- hold = payout requested
- release = failed payout returned

This creates full money trail and audit history.

## 2. Lock

Used:

```python
with transaction.atomic():
    merchant = Merchant.objects.select_for_update().get(id=merchant_id)


This locks merchant row during payout request.

If two requests come together, second waits until first finishes.

This prevents overdrawing.

3. Idempotency

Merchant sends header:

Idempotency-Key

System checks existing payout with same key.

If found, returns old payout response.

No duplicate payout created.

4. State Machine

Payout statuses:

pending
completed
failed

Background worker moves pending payouts to completed or failed.

Failed payout returns funds using release ledger entry.

5. AI Audit

AI initially suggested checking balance in Python without locking.

That would allow race condition.

I replaced it using:

transaction.atomic()
select_for_update()

This ensures correct concurrent payout handling.