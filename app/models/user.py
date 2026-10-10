from datetime import datetime

from flask_login import UserMixin

from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(
        db.String(20),
        db.CheckConstraint("role IN ('student', 'faculty', 'admin')", name="ck_users_role"),
        nullable=False,
    )
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    student = db.relationship("Student", back_populates="user", uselist=False)
    faculty = db.relationship("Faculty", back_populates="user", uselist=False)
    created_notices = db.relationship("Notice", back_populates="creator")
    created_events = db.relationship("Event", back_populates="creator")
    marked_attendance = db.relationship("Attendance", back_populates="marker")
