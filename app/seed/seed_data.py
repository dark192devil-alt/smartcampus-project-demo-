from datetime import date, datetime, time, timedelta
import os
import secrets

from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models import (
    Assignment,
    AssignmentSubmission,
    Attendance,
    Course,
    Enrollment,
    Event,
    EventRegistration,
    Exam,
    Faculty,
    Notice,
    Student,
    Subject,
    Timetable,
    User,
)


DEMO_EMAILS = {
    "admin": "admin@smartcampus.test",
    "faculty": "faculty@smartcampus.test",
    "student": "student@smartcampus.test",
}


def update_demo_passwords():
    demo_password = os.getenv("DEMO_PASSWORD")
    if not demo_password:
        return False

    users = User.query.filter(User.email.in_(DEMO_EMAILS.values())).all()
    if len(users) != len(DEMO_EMAILS):
        return False

    for user in users:
        user.password_hash = generate_password_hash(demo_password)
    db.session.commit()
    return True


def update_demo_student_name():
    student_user = User.query.filter_by(email=DEMO_EMAILS["student"]).first()
    if student_user is None or student_user.name == "Student":
        return False

    student_user.name = "Student"
    db.session.commit()
    return True


def seed_database():
    if Course.query.first() is not None:
        return False

    admin_user = User(
        name="SmartCampus Admin",
        email="admin@smartcampus.test",
        password_hash=generate_password_hash(secrets.token_urlsafe(24)),
        role="admin",
    )
    faculty_user = User(
        name="Asha Deshmukh",
        email="faculty@smartcampus.test",
        password_hash=generate_password_hash(secrets.token_urlsafe(24)),
        role="faculty",
    )
    student_user = User(
        name="Student",
        email="student@smartcampus.test",
        password_hash=generate_password_hash(secrets.token_urlsafe(24)),
        role="student",
    )
    db.session.add_all([admin_user, faculty_user, student_user])
    db.session.flush()

    faculty = Faculty(
        user_id=faculty_user.id,
        employee_number="FAC-001",
        department="Commerce",
    )
    course = Course(
        name="HSC Commerce",
        department="Commerce",
        duration_years=2,
    )
    db.session.add_all([faculty, course])
    db.session.flush()

    student = Student(
        user_id=student_user.id,
        student_number="STU-001",
        course_id=course.id,
        year="11th",
        division="A",
    )
    subject = Subject(
        name="Information Technology (IT)",
        course_id=course.id,
        faculty_id=faculty.id,
    )
    db.session.add_all([student, subject])
    db.session.flush()

    assignment = Assignment(
        subject_id=subject.id,
        faculty_id=faculty.id,
        title="Introduction to Journal Entries",
        description="Prepare five example journal entries.",
        due_date=date.today() + timedelta(days=14),
    )
    event = Event(
        title="Commerce Exhibition Orientation",
        description="Orientation for the annual college exhibition.",
        event_date=datetime.now() + timedelta(days=7),
        location="Seminar Hall",
        created_by=admin_user.id,
    )
    db.session.add_all([assignment, event])
    db.session.flush()

    db.session.add_all(
        [
            Enrollment(
                student_id=student.id,
                subject_id=subject.id,
                academic_year="2026-27",
            ),
            Attendance(
                student_id=student.id,
                subject_id=subject.id,
                marked_by=faculty_user.id,
                date=date.today(),
                status="present",
            ),
            AssignmentSubmission(
                assignment_id=assignment.id,
                student_id=student.id,
                status="submitted",
            ),
            EventRegistration(event_id=event.id, student_id=student.id),
            Notice(
                title="Welcome to SmartCampus",
                content="This fictional notice verifies the notice table and creator relationship.",
                created_by=admin_user.id,
                target_role="all",
            ),
            Timetable(
                course_id=course.id,
                subject_id=subject.id,
                faculty_id=faculty.id,
                day="Monday",
                start_time=time(9, 0),
                end_time=time(10, 0),
                room="C-101",
            ),
            Exam(
                subject_id=subject.id,
                course_id=course.id,
                title="Information Technology (IT) Internal Test",
                exam_type="internal",
                exam_date=date.today() + timedelta(days=30),
                start_time=time(10, 0),
                end_time=time(11, 0),
                room="C-101",
            ),
        ]
    )
    db.session.commit()
    return True
