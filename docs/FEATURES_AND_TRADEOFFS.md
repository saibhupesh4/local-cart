# Features, advantages and tradeoffs

## Present features

Catalog/category browsing, product images and gallery, variations, text search, reviews, custom email-based accounts, account activation/password reset, profile editing, session/user carts, checkout form, order history/details, admin and a demonstrative payment/order completion flow are present in code. `seed_demo_catalog` creates a safe sample catalog and common demo sizes without importing private database records. Cart and order tables are horizontally scrollable on narrow screens. Dark mode uses a persistent browser preference and shared CSS variables.

## Advantages

The repository provides an end-to-end Django learning example with separate apps, conventional URL/view/model/template layers, migrations, custom user model, ORM relationships, forms, sessions, messages, static/media files and server-rendered pages. It can be run locally without configuring cloud storage or SMTP after dependencies are installed.

## Limitations

The project retains tutorial-era Django and package pins, duplicated asset trees, incomplete test coverage, and several fragile request-handling patterns. The payment flow does not verify provider transactions and must not process real money. There is no stock reservation, robust transaction boundary, production hardening, deployment setup or real email requirement. Product/order currency and price precision should be reviewed. Existing category pagination is unusually small and UI content quality depends on fixture data.

## What changed in this pass

Settings now default to local storage/email/hosts, the shared shell no longer advertises an unrelated course or embeds a public payment SDK key, theme switching is implemented, empty search no longer crashes, registration form cleaning works, username derives from full email, and account order lookup enforces ownership. Documentation and focused tests were added. These are directly verifiable changes; no claim of production readiness is made.
