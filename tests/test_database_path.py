import tempfile
import unittest
from pathlib import Path

from config import DATABASE_PATH, INSTANCE_DIR, ensure_instance_directory


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


if __name__ == "__main__":
    unittest.main()