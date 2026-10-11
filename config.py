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
configured_secret = os.getenv("SECRET_KEY")
if SMARTCAMPUS_ENV == "production" and not configured_secret:
    raise RuntimeError("SECRET_KEY must be set when SMARTCAMPUS_ENV=production")


class Config:
    SECRET_KEY = configured_secret or "local-development-secret"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH.as_posix()}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = SMARTCAMPUS_ENV == "production"
