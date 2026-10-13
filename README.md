# Playto Payout Engine

A payout-processing project that demonstrates merchant balances, ledger entries, idempotency and payout state transitions.

## Live demo

**https://payout-engine-sankalp.vercel.app/**

The public demo is a deterministic payout sandbox.

It stores only demo state in the visitor's browser and does not move real money.

## What the live demo shows

- merchant available balance,
- append-style ledger entries,
- payout creation,
- HOLD entries,
- idempotency-key replay protection,
- pending payout processing,
- COMPLETED + DEBIT settlement,
- FAILED + RELEASE recovery,
- insufficient-balance rejection.

## Core idempotency rule

If the same merchant sends the same idempotency key again, the system returns the existing payout instead of reserving the balance a second time.

## Original backend

The original reference implementation is still in the repository.

It uses:

- Django
- Django REST Framework
- Django ORM
- SQLite
- transactional payout logic
- idempotency keys
- background-style payout processing.

The browser demo is an additional public portfolio interface; it does not replace the backend source.

## Run the browser demo locally

```bash
cd web
python -m http.server 8000
```

Open:

```text
http://localhost:8000
```

## Run the original Django backend

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Production notes

A real payout service would additionally need:

- a production database such as PostgreSQL,
- secure authentication and authorization,
- a durable job queue,
- provider integrations,
- reconciliation,
- audit/security controls,
- monitoring and alerting.

## Author

**Sankalp Gupta**

- GitHub: https://github.com/Sankalp-gupta1
- LinkedIn: https://www.linkedin.com/in/sankalp-gupta-rishi-8617302b0/


## Run the web demo locally

The hosted portfolio version is a static web demo, so it does not need an API key or database for local preview.

### Step 1 — clone the repository

```bash
git clone https://github.com/Sankalp-gupta1/Initial-Playto-payout-engine-submission.git
cd Initial-Playto-payout-engine-submission
```

### Step 2 — open the deployable web folder

```bash
cd web
```

### Step 3 — start a small local server

```bash
python -m http.server 8000
```

### Step 4 — open the app

```text
http://localhost:8000
```

Production demo: **https://payout-engine-sankalp.vercel.app/**

The original project files are kept in the repository. The `web/` version is the browser-friendly deployment made for easy review.
