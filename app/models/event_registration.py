from datetime import datetime

from app.extensions import db


class EventRegistration(db.Model):
    __tablename__ = "event_registrations"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    registered_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default="registered")
    __table_args__ = (
        db.UniqueConstraint("event_id", "student_id", name="uq_event_student_registration"),
        db.CheckConstraint(
            "status IN ('registered', 'cancelled', 'attended')", name="ck_registration_status"
        ),
    )

    event = db.relationship("Event", back_populates="registrations")
    student = db.relationship("Student", back_populates="event_registrations")
