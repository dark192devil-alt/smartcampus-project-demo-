from datetime import date

from flask import Blueprint, render_template, request
from flask_login import current_user

from app.models import Subject
from app.services.student_service import (
    get_assignments,
    get_attendance_data,
    get_dashboard_data,
    get_events,
    get_exams,
    get_notices,
    get_student,
    get_timetable,
)
from app.utils.decorators import role_required


student_bp = Blueprint("student", __name__, url_prefix="/student")


@student_bp.route("/dashboard")
@role_required("student")
def dashboard():
    student = get_student(current_user.student.id)
    data = get_dashboard_data(student)
    return render_template("student/dashboard.html", student=student, today=date.today(), **data)


@student_bp.route("/attendance")
@role_required("student")
def attendance():
    student = get_student(current_user.student.id)
    return render_template("student/attendance.html", student=student, **get_attendance_data(student))


@student_bp.route("/assignments")
@role_required("student")
def assignments():
    student = get_student(current_user.student.id)
    subject_id = request.args.get("subject", type=int)
    status = request.args.get("status", "").strip().lower() or None
    subjects = [enrollment.subject for enrollment in student.enrollments if enrollment.status == "active"]
    return render_template(
        "student/assignments.html",
        student=student,
        assignments=get_assignments(student, subject_id=subject_id, status=status),
        subjects=subjects,
        selected_subject=subject_id,
        selected_status=status,
    )


@student_bp.route("/exams")
@role_required("student")
def exams():
    student = get_student(current_user.student.id)
    return render_template("student/exams.html", student=student, exams=get_exams(student))


@student_bp.route("/timetable")
@role_required("student")
def timetable():
    student = get_student(current_user.student.id)
    return render_template("student/timetable.html", student=student, timetable=get_timetable(student))


@student_bp.route("/notices")
@role_required("student")
def notices():
    return render_template("student/notices.html", notices=get_notices())


@student_bp.route("/events")
@role_required("student")
def events():
    return render_template("student/events.html", events=get_events())


@student_bp.route("/assistant")
@role_required("student")
def assistant():
    return render_template("student/assistant.html")
