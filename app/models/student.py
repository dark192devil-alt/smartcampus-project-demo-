from datetime import datetime

from app.extensions import db


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    student_number = db.Column(db.String(50), nullable=False, unique=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    year = db.Column(db.String(20), nullable=False)
    division = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship("User", back_populates="student")
    course = db.relationship("Course", back_populates="students")
    enrollments = db.relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")
    attendance_records = db.relationship("Attendance", back_populates="student", cascade="all, delete-orphan")
    submissions = db.relationship("AssignmentSubmission", back_populates="student", cascade="all, delete-orphan")
    event_registrations = db.relationship("EventRegistration", back_populates="student", cascade="all, delete-orphan")
