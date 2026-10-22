# Local setup and troubleshooting

## Windows with Anaconda

Use the existing `django_env` Conda environment from the project directory:

```powershell
conda activate django_env
python -m pip install -r requirements.txt  # only if dependencies are missing
python manage.py migrate
python manage.py seed_demo_catalog
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. The catalog command creates sample categories and products, copies bundled demo images from `greatkart/static/images/items/` to local media, and creates standard sample sizes. It does not load accounts, orders, payments or sessions. It can be run more than once without duplicating its records.

The default configuration uses SQLite, local static/media paths, localhost hosts and console email. Activation and password-reset emails appear in the runserver console. A newly registered account must be activated before login. `.env-sample` documents optional local settings; `.env` is ignored and should never be committed.

## Checks

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

The current local verification passed all three commands; the test suite has 12 passing tests. Django tests use a separate temporary database.

## Common issues

- **Django import error:** confirm `conda activate django_env` and run `python -m django --version` from the same terminal.
- **No products after migration:** run `python manage.py seed_demo_catalog`.
- **Login rejected after registration:** activate the account using the link in the runserver console. The local email backend prints messages instead of sending them.
- **Missing product images:** rerun `python manage.py seed_demo_catalog`; source images must exist in `greatkart/static/images/items/`.
- **Database questions:** keep `db.sqlite3` if it contains useful local data. It is ignored by Git, as are `media/`, environment directories, logs and `data.json`.

`python manage.py createsuperuser` creates an admin account. The admin interface is at `/securelogin/`. The optional PostgreSQL configuration activates when `RDS_DB_NAME` is set and requires all RDS settings and a compatible driver.
