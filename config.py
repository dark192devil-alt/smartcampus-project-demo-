from pathlib import Path
import os

from dotenv import load_dotenv


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent


def ensure_instance_directory(instance_dir):
    instance_dir.mkdir(parents=True, exist_ok=True)
    return instance_dir


INSTANCE_DIR = ensure_instance_directory(BASE_DIR / "instance")
DATABASE_PATH = INSTANCE_DIR / "smartcampus.db"
SMARTCAMPUS_ENV = os.getenv("SMARTCAMPUS_ENV", "development").lower()


def resolve_database_uri(database_url, sqlite_path):
    """Use a hosted PostgreSQL URL when configured, otherwise local SQLite."""
    database_url = (database_url or "").strip()
    if not database_url:
        return f"sqlite:///{sqlite_path.as_posix()}"

    # Providers may give SQLAlchemy a generic PostgreSQL URL. Pin psycopg 3
    # explicitly so Render installs and uses the driver in requirements.txt.
    if database_url.startswith("postgres://"):
        return "postgresql+psycopg://" + database_url[len("postgres://") :]
    if database_url.startswith("postgresql://"):
        return "postgresql+psycopg://" + database_url[len("postgresql://") :]
    return database_url


def resolve_secret_key(environment, secret_key):
    if environment == "production" and (
        not secret_key or secret_key == "local-development-secret"
    ):
        raise RuntimeError(
            "SECRET_KEY must be set to a non-default value when SMARTCAMPUS_ENV=production"
        )
    return secret_key or "local-development-secret"


configured_secret = resolve_secret_key(
    SMARTCAMPUS_ENV, os.getenv("SECRET_KEY")
)


class Config:
    SECRET_KEY = configured_secret
    SQLALCHEMY_DATABASE_URI = resolve_database_uri(
        os.getenv("DATABASE_URL"), DATABASE_PATH
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    AUTO_CREATE_SCHEMA = SMARTCAMPUS_ENV == "production"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = SMARTCAMPUS_ENV == "production"
