from datetime import datetime

from app.extensions import db


class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id"), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    __table_args__ = (
        db.UniqueConstraint("name", "course_id", name="uq_subject_name_course"),
    )

    course = db.relationship("Course", back_populates="subjects")
    faculty = db.relationship("Faculty", back_populates="subjects")
    enrollments = db.relationship("Enrollment", back_populates="subject", cascade="all, delete-orphan")
    attendance_records = db.relationship("Attendance", back_populates="subject", cascade="all, delete-orphan")
    assignments = db.relationship("Assignment", back_populates="subject", cascade="all, delete-orphan")
    timetable_entries = db.relationship("Timetable", back_populates="subject")
    exams = db.relationship("Exam", back_populates="subject")
