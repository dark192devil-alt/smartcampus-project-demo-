from datetime import datetime

from app.extensions import db


class Enrollment(db.Model):
    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    academic_year = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="active")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    __table_args__ = (
        db.UniqueConstraint(
            "student_id", "subject_id", "academic_year", name="uq_student_subject_year"
        ),
        db.CheckConstraint("status IN ('active', 'completed', 'dropped')", name="ck_enrollment_status"),
    )

    student = db.relationship("Student", back_populates="enrollments")
    subject = db.relationship("Subject", back_populates="enrollments")
