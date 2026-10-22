# Project structure

```text
greatkart-local-store/
├── manage.py                 Django command entry point
├── requirements.txt          Python dependencies
├── .env-sample               local configuration example
├── .gitignore                local/generated-file exclusions
├── data.json                 local export with account/order data; ignored and not used for seeding
├── greatkart/                project settings, root URLs, home, WSGI/ASGI, site assets
├── accounts/                 custom user, profile, forms, account views, migrations, tests
├── category/                 category model, menu context processor, migrations
├── store/                    catalog, review/gallery models, forms, views, migrations, tests
├── carts/                    session cart models, views, context processor, migrations
├── orders/                   order/payment models, billing form, views, migrations
├── templates/                shared base, account, store, cart, order and include templates
├── static/                   legacy duplicate asset tree; not configured as site source
├── .ebextensions/            legacy Elastic Beanstalk configuration
└── docs/                     maintained project documentation
```

Edit Python modules, templates, `greatkart/static/css/custom.css`, `greatkart/static/js/script.js`, tests and documentation during normal feature work. Migrations are generated schema history; do not edit/delete old migrations casually. `staticfiles/`, `media/`, virtual environments, caches and `db.sqlite3` are runtime/local data and ignored. The ignored `data.json` contains personal and transactional records; run `python manage.py seed_demo_catalog` for safe sample catalog data. `.ebextensions/` is historical deployment material, not used in local execution. The adjacent `greatkart-course-main/` source copy is excluded from version control.
