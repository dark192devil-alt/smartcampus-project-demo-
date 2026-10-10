# SmartCampus

SmartCampus is a Flask college management application with Student, Faculty, Admin, and local academic assistant features.

## Initialize the database

```text
python -m app.seed.initialize_db
```

This creates `instance/smartcampus.db` and inserts a small set of fictional records.

## Run the application

```text
python run.py
```

Local development defaults to `127.0.0.1:5000`. Set `HOST`, `PORT`, and `FLASK_DEBUG` when needed.

## Deployment readiness

Install dependencies with `pip install -r requirements.txt`. A compatible production WSGI server command is:

```text
gunicorn --bind 0.0.0.0:$PORT run:app
```

Set `SMARTCAMPUS_ENV=production` and provide a real `SECRET_KEY` through the hosting platform environment. The application keeps SQLite for local/demo use; its local database is ignored by Git and should not be treated as permanent storage on an ephemeral hosting filesystem.

`GET /health` returns a minimal unauthenticated health response. SmartCampus is deployment-prepared but is not claimed to be deployed.
