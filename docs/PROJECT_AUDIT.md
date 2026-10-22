# Project audit

## Baseline

The application lives at the root of `greatkart-local-store/`. The adjacent `greatkart-course-main/` source copy is excluded from the Git repository. The local database, media uploads, environment packages, logs and `data.json` are ignored. The JSON export contains account, session, admin-login, order and payment records, so it is not needed to seed the demo storefront. Local development uses the existing Anaconda `django_env` environment. The current check and migration-drift commands pass, and the test suite has 12 passing tests.

## Architecture and feature inventory

The project is a conventional Django template application. `greatkart` holds settings, root routes and home page; `category` provides category records and menu context; `accounts` defines the custom `Account` user and profile/account flows; `store` owns products, variations, reviews and gallery; `carts` owns session/user cart behavior and a cart-count context processor; `orders` owns billing, demo payment and order records. Templates are shared in root `templates/`; site assets are in `greatkart/static/`. SQLite is the local default; settings also contain an optional RDS PostgreSQL branch.

Implemented flows include catalog/category browsing, search, product detail, variations, reviews, registration and email activation, login/logout, password reset/change, user profile, cart, checkout preview, order persistence, demo payment record, order history and Django admin behind `/securelogin/` with a honeypot at `/admin/`.

## Confirmed defects and risks

* Local settings default to local static/media storage and console email, with a local-only fallback secret. Activation and password-reset emails print in the development server console.
* `store.search` used `products`/`product_count` before assignment when `keyword` was missing, and did not restrict results to available products. It now handles an empty query and filters available items.
* `RegistrationForm.clean()` did not return cleaned data. It now returns it. User creation did not set required `phone_number` before saving, so registration could fail with an integrity error; the account manager now accepts the phone field and registration supplies it. Registration uses full email as username to avoid collisions between different addresses with the same prefix.
* `accounts.order_detail` looked up order lines by public order number without confirming order ownership. It now scopes lookup to the signed-in user and completed orders.
* The shared layout previously embedded a PayPal client identifier. The real payment capture flow was replaced with an explicit local demo-order action; the server now generates its own demo transaction ID, checks order ownership and stock, and groups database writes in a transaction. No payment is collected.
* Email sending happens after the order transaction and can still fail after order completion. Product pricing uses integer/float fields and needs a currency/precision review.
* Some broad exception handling, GET-based cart mutations, route-level access gaps, repeated cart arithmetic and account/order edge cases remain candidates for follow-up.
* Settings previously allowed every host and hard-coded an Elastic Beanstalk host. Hosts are now explicit local defaults, but the settings still need a production security review before any deployment.

## Potential cleanup and rationale

Keep both `static/` and `greatkart/static/`: the former includes Django admin assets while the latter contains configured site assets. The ignored `data.json` is not a safe fixture because it also contains personal and transactional records. Use `python manage.py seed_demo_catalog` to create the safe storefront sample data. Existing migrations are historical schema and remain intact.

## Changes made

Local-first settings, removal of third-party course promotion and external payment capture, a local-only demo order flow, theme toggle and theme styles, GreatKart footer identity, empty-search fix, registration form fix, unique email-derived username, order ownership check, responsive table layouts, login redirect handling, demo catalog/size seeding, and tests for catalog, authentication, cart behavior and order flow. No dependency was added or removed.
