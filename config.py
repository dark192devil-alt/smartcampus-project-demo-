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
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH.as_posix()}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUTO_CREATE_SCHEMA = SMARTCAMPUS_ENV == "production"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = SMARTCAMPUS_ENV == "production"
