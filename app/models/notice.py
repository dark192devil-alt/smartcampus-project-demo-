from datetime import datetime

from app.extensions import db


class Notice(db.Model):
    __tablename__ = "notices"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    target_role = db.Column(db.String(20), nullable=False, default="all")
    published_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    __table_args__ = (
        db.CheckConstraint(
            "target_role IN ('all', 'student', 'faculty', 'admin')",
            name="ck_notice_target_role",
        ),
    )

    creator = db.relationship("User", back_populates="created_notices")
