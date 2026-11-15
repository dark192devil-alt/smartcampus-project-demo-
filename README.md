# SmartCampus

SmartCampus is a Flask college management application with Student, Faculty, Admin, and local academic assistant features.

## Initialize the database locally

```text
python -m app.seed.initialize_db
```

This creates `instance/smartcampus.db` and inserts a small set of fictional records.

## Run the application

```text
python run.py
```

Local development defaults to `127.0.0.1:5000`. Set `HOST`, `PORT`, and `FLASK_DEBUG` when needed.

## Deployment with PostgreSQL

The app uses local SQLite when `DATABASE_URL` is not set. For a hosted database, set `DATABASE_URL` in the hosting service's environment variables and install dependencies from `requirements.txt`. PostgreSQL URLs beginning with `postgres://` or `postgresql://` are supported.

For Supabase with Render, use the **Session pooler** connection string from the Supabase project's **Connect** panel. Render's free web service uses an IPv4-only network, while Supabase's direct connection is IPv6 by default. Keep the connection string private and add it as the Render `DATABASE_URL` value; do not commit it to this repository.

Set `SMARTCAMPUS_ENV=production`, a strong `SECRET_KEY`, and `DEMO_PASSWORD` in Render's environment. On production startup, the app creates missing tables and inserts the fictional demo records into an empty database. It then applies `DEMO_PASSWORD` to the three demo accounts. The seed step is idempotent for an already populated database.

Supabase's Free plan can pause a project after a week of low activity. Resume it from the Supabase dashboard if that happens. The free database is separate from Render's filesystem, so Render restarts and deploys do not erase it.

## Deployment command

```text
gunicorn --bind 0.0.0.0:$PORT run:app
```

`GET /health` returns a minimal unauthenticated health response.
