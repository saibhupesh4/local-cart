# GreatKart Local Store

GreatKart Local Store is an existing Django e-commerce tutorial project, improved as a locally runnable learning and portfolio codebase. It demonstrates catalog browsing, account flows, a session-aware cart, checkout and order records. Checkout is a **demonstration only**: there is no verified real payment processing and the project is not production-ready.

## Features

- Product catalog, category browsing, search, product variations, images and reviews.
- Custom email-login accounts, activation/reset flows and profile/order pages.
- Anonymous and signed-in carts, billing form, demo order/payment records.
- Category-appropriate sample sizes for demo clothing, jeans and shoes.
- Django admin, local-first configuration, responsive cart/order tables and a persistent light/dark theme toggle.

This pass fixes empty search handling, form cleaning for registration, username collisions and order ownership checks. It replaces the external PayPal capture flow with a local-only demo order operation and removes unrelated course promotion. It adds focused automated tests and detailed technical documentation.

## Technology

Python, Django 3.1 (pinned), Django templates and ORM, SQLite locally, optional PostgreSQL through existing RDS environment configuration, Bootstrap-based CSS, JavaScript and Pillow for images. Dependencies are listed in `requirements.txt`.

## Run locally

Use the existing Anaconda environment. In PowerShell:

```powershell
conda activate django_env
# Install dependencies only if they are missing from this environment:
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo_catalog
python manage.py runserver
```

Run these commands from the folder containing `manage.py`. Visit `http://127.0.0.1:8000/`. Local defaults use SQLite, local static/media files, localhost hosts and console email (activation/reset emails appear in the server console). `seed_demo_catalog` creates only sample categories/products, copies bundled sample images to ignored local media, and adds sample sizes. It does not import account, order, payment or session data. Copy `.env-sample` to `.env` only when setting local overrides; `.env` is ignored by Git. The fallback secret key is for local evaluation only. Admin is at `/securelogin/`; create an account with `python manage.py createsuperuser`.

Run checks with `python manage.py check`, `python manage.py makemigrations --check --dry-run`, and `python manage.py test`. The current audit passes all three checks, with 12 passing tests. Existing database files, local media uploads, environment folders and the account/order export `data.json` are local data and should not be committed.

## Dark mode

Use the “Dark mode” button in the header. The selected theme is saved in browser local storage and applies to the shared shell and common Bootstrap surfaces. Some legacy components may need further contrast-specific styling.

## Known limitations

The checkout records a demo order only; it does not connect to a payment provider or collect money. Sample size choices are demonstration data and do not represent per-size inventory. Some tutorial-era routes and exception handling remain fragile; further stock and cart constraints need review. The project targets local evaluation rather than deployment.

## Architecture at a glance

`manage.py` starts Django configured by `greatkart.settings`. Root URL routes dispatch to `category`, `accounts`, `store`, `carts` and `orders`; views use the ORM and render shared templates. Anonymous cart identity is held in a session. See [architecture](docs/ARCHITECTURE.md).

## Documentation

- [Project audit](docs/PROJECT_AUDIT.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Project structure](docs/PROJECT_STRUCTURE.md)
- [Database schema](docs/DATABASE_SCHEMA.md)
- [URL routing](docs/URL_ROUTING.md)
- [Function reference](docs/FUNCTION_REFERENCE.md)
- [Request and data flows](docs/REQUEST_AND_DATA_FLOWS.md)
- [Error handling and security](docs/ERROR_HANDLING_AND_SECURITY.md)
- [Setup and troubleshooting](docs/SETUP_AND_TROUBLESHOOTING.md)
- [Features and tradeoffs](docs/FEATURES_AND_TRADEOFFS.md)

## Source control exclusions

The source copy in `greatkart-course-main/` is excluded from this repository. Local databases, media uploads, environment folders, logs and `data.json` are ignored; `data.json` contains account/session/order records. Keep those files out of public commits.
