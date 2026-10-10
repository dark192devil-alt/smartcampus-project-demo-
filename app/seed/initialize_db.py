from app import create_app
from app.extensions import db
from app.seed.seed_data import (
    seed_database,
    update_demo_passwords,
    update_demo_student_name,
)


app = create_app()


with app.app_context():
    db.create_all()
    seeded = seed_database()
    passwords_updated = update_demo_passwords()
    student_name_updated = update_demo_student_name()
    if seeded:
        print("Database initialized and sample data inserted.")
    else:
        print("Database already contains data; no seed changes made.")
    if passwords_updated:
        print("Demo account passwords updated from DEMO_PASSWORD.")
    if student_name_updated:
        print("Demo student name updated to Student.")
