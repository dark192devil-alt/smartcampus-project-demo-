from datetime import datetime

from app.extensions import db


class Assignment(db.Model):
    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    subject = db.relationship("Subject", back_populates="assignments")
    creator = db.relationship("Faculty", back_populates="assignments")
    submissions = db.relationship(
        "AssignmentSubmission", back_populates="assignment", cascade="all, delete-orphan"
    )
