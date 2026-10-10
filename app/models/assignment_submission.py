from datetime import datetime

from app.extensions import db


class AssignmentSubmission(db.Model):
    __tablename__ = "assignment_submissions"

    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignments.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    file_path = db.Column(db.String(500), nullable=True)
    submitted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default="submitted")
    remarks = db.Column(db.Text, nullable=True)
    __table_args__ = (
        db.UniqueConstraint("assignment_id", "student_id", name="uq_assignment_student_submission"),
        db.CheckConstraint(
            "status IN ('submitted', 'reviewed', 'late')", name="ck_submission_status"
        ),
    )

    assignment = db.relationship("Assignment", back_populates="submissions")
    student = db.relationship("Student", back_populates="submissions")
