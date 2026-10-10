from datetime import datetime

from app.extensions import db


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    department = db.Column(db.String(120), nullable=False)
    duration_years = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    students = db.relationship("Student", back_populates="course")
    subjects = db.relationship("Subject", back_populates="course")
    timetable_entries = db.relationship("Timetable", back_populates="course")
    exams = db.relationship("Exam", back_populates="course")
