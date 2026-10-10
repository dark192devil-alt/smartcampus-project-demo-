from datetime import datetime

from app.extensions import db


class Faculty(db.Model):
    __tablename__ = "faculty"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    employee_number = db.Column(db.String(50), nullable=False, unique=True)
    department = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship("User", back_populates="faculty")
    subjects = db.relationship("Subject", back_populates="faculty")
    assignments = db.relationship("Assignment", back_populates="creator")
    timetable_entries = db.relationship("Timetable", back_populates="faculty")
