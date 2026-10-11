import tempfile
import unittest
from pathlib import Path

from app import create_app
from config import DATABASE_PATH, INSTANCE_DIR, ensure_instance_directory
from app.extensions import db
from app.models import User


class DatabasePathTests(unittest.TestCase):
    def test_instance_directory_is_created_for_a_new_path(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            instance_dir = Path(temporary_directory) / "missing" / "instance"

            result = ensure_instance_directory(instance_dir)

            self.assertEqual(result, instance_dir)
            self.assertTrue(instance_dir.is_dir())

    def test_sqlite_path_is_inside_instance_directory(self):
        self.assertTrue(INSTANCE_DIR.is_dir())
        self.assertEqual(DATABASE_PATH.parent, INSTANCE_DIR)
        self.assertEqual(DATABASE_PATH.name, "smartcampus.db")

    def test_production_startup_creates_schema_idempotently(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "render.sqlite"
            test_config = type(
                "TemporaryProductionConfig",
                (),
                {
                    "TESTING": True,
                    "SECRET_KEY": "isolated-test-secret",
                    "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path.as_posix()}",
                    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
                    "AUTO_CREATE_SCHEMA": True,
                },
            )

            app = create_app(test_config)
            with app.app_context():
                self.assertIn("users", db.inspect(db.engine).get_table_names())
                db.session.add(
                    User(
                        name="Schema Test User",
                        email="schema-test@example.test",
                        password_hash="not-a-real-account-password",
                        role="admin",
                    )
                )
                db.session.commit()
                db.session.remove()
                db.engine.dispose()

            restarted_app = create_app(test_config)
            with restarted_app.app_context():
                self.assertEqual(User.query.filter_by(email="schema-test@example.test").count(), 1)
                db.session.remove()
                db.engine.dispose()


if __name__ == "__main__":
    unittest.main()