# Finance Backend

## Populate SQLite with sample data

Run this single command to create sample users and transactions:

```bash
python manage.py populate_db
```

It creates these 3 users:
- `analyst`
- `viewer`
- `admin`

All three users use the same password:

```bash
SeedPass@123
```

If this is a fresh database, run migrations first:

```bash
python manage.py migrate
```
