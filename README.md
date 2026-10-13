# Playto Payout Engine

## Live app

**https://payout-engine-sankalp.vercel.app/**

The hosted sandbox visualizes the payout state machine documented in the Django backend:

- append-style ledger
- available balance derived from ledger entries
- idempotency-key replay protection
- HOLD on payout creation
- COMPLETED + DEBIT settlement
- FAILED + RELEASE recovery
- insufficient-balance rejection

The original Django/DRF implementation remains in the repository as the backend reference. The browser version is a deterministic public demo and stores only local demo state in the visitor's browser.

### Run the web demo locally

```bash
cd web
python -m http.server 8000
```

---

A payout-processing project that demonstrates merchant balances, ledger entries, idempotency and payout state transitions.

## Live demo


## Original backend

The original reference implementation uses:

- Django
- Django REST Framework
- Django ORM
- SQLite
- row-level / transactional payout logic
- idempotency keys
- pending payout processing

Those files remain unchanged in the repository.

## Deployed simulator

The `web/` version provides a zero-secret interactive demo for recruiters.

It lets you:

- create a payout,
- reserve funds,
- replay the same idempotency key,
- verify that duplicate requests do not reserve money twice,
- process pending payouts,
- inspect the ledger,
- see available and reserved balances.

The simulator stores demo state in the browser. It does not move real money.

## Core rule

For the same merchant and idempotency key, a repeated request returns the existing payout instead of creating a second payout.

## Run locally

```bash
cd web
python -m http.server 8000
```

Open `http://localhost:8000`.

## Run the original Django backend

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Author

Sankalp Gupta  
GitHub: https://github.com/Sankalp-gupta1
