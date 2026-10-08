# Playto Payout Engine

A minimal Django payout engine that models **merchant balances, ledger entries, idempotent payout requests, row-level locking, payout state transitions, and background processing**.

## Overview

The project is designed around an append-style ledger rather than a single mutable balance field.

A merchant's available balance is derived from ledger entries:

- `credit` — funds added
- `hold` — funds reserved for a pending payout
- `debit` — funds permanently deducted after a successful payout
- `release` — held funds returned after a failed payout

## Core Features

- Merchant balance calculation from ledger history
- Payout request API
- Idempotency-key support
- Row-level concurrency protection with `select_for_update()`
- Atomic payout creation
- Insufficient-balance protection
- Pending / completed / failed payout states
- Background payout processor
- Automated tests for idempotency and insufficient balance

## Tech Stack

- Python
- Django
- Django REST Framework
- Django ORM
- SQLite for the current local configuration
- Gunicorn

## Data Model

### Merchant

Represents the account that owns funds and requests payouts.

### Ledger

Stores balance-changing entries linked to a merchant.

### Payout

Stores:

- merchant
- amount in paise
- bank account ID
- idempotency key
- payout status
- creation timestamp

## Payout State Flow

```text
Payout request
     │
     ▼
Validate idempotency key
     │
     ▼
Lock merchant row
     │
     ▼
Calculate available balance
     │
     ├── insufficient ──► reject
     │
     ▼
Create pending payout
     │
     ▼
Create HOLD ledger entry
     │
     ▼
Background processor
     │
     ├── success ──► COMPLETED + DEBIT
     │
     └── failure ──► FAILED + RELEASE
```

## Concurrency Protection

Payout creation runs inside:

```python
with transaction.atomic():
    merchant = Merchant.objects.select_for_update().get(id=merchant_id)
```

This locks the merchant row while the request checks the balance and creates the payout, preventing concurrent requests from independently spending the same available funds.

## Idempotency

Clients can send:

```text
Idempotency-Key: unique-request-key
```

If a payout already exists for the same merchant and key, the existing payout is returned instead of creating a duplicate.

## API Endpoints

### Get Merchant Balance

```http
GET /api/balance/<merchant_id>/
```

Example response:

```json
{
  "merchant": "Test Merchant",
  "balance_paise": 100000
}
```

### Create Payout

```http
POST /api/payout/<merchant_id>/
Idempotency-Key: payout-001
Content-Type: application/json
```

Example body:

```json
{
  "amount_paise": 50000,
  "bank_account_id": "bank-account-reference"
}
```

## Setup

Clone the repository:

```bash
git clone https://github.com/Sankalp-gupta1/Initial-Playto-payout-engine-submission.git
cd Initial-Playto-payout-engine-submission
```

Create a virtual environment:

```bash
python -m venv .venv
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Start the server:

```bash
python manage.py runserver
```

## Process Pending Payouts

The repository includes a Django management command that processes pending payouts:

```bash
python manage.py process_payouts
```

The current prototype simulates payout outcomes and updates the ledger accordingly.

## Tests

Run:

```bash
python manage.py test
```

Included tests cover:

- repeated requests using the same idempotency key
- insufficient balance rejection

## Engineering Decision

A balance check without locking can introduce a race condition when two payout requests arrive at the same time.

This implementation uses `transaction.atomic()` and `select_for_update()` so that balance validation and payout creation occur while the merchant row is locked.

## Production Notes

This repository is a compact backend prototype. A production payout service would additionally require:

- externalized secrets
- PostgreSQL or another production database
- authentication and authorization
- durable background queues
- provider integration
- deterministic provider reconciliation
- observability and audit tooling
- more extensive concurrency and failure testing

## Author

**Sankalp Gupta**

GitHub: https://github.com/Sankalp-gupta1
