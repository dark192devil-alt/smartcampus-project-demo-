from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user

from app.extensions import db
from app.models import Assignment
from app.services.faculty_service import (
    attendance_data,
    dashboard_data,
    get_assignments,
    get_exams,
    get_faculty,
    get_notices,
    get_submissions,
    get_subjects,
)
from app.utils.decorators import role_required


faculty_bp = Blueprint("faculty", __name__, url_prefix="/faculty")


@faculty_bp.route("/dashboard")
@role_required("faculty")
def dashboard():
    faculty = get_faculty(current_user.faculty.id)
    return render_template("faculty/dashboard.html", faculty=faculty, today=date.today(), **dashboard_data(faculty))


@faculty_bp.route("/attendance")
@role_required("faculty")
def attendance():
    faculty = get_faculty(current_user.faculty.id)
    return render_template("faculty/attendance.html", **attendance_data(faculty, request.args.get("subject", type=int)))


@faculty_bp.route("/assignments")
@role_required("faculty")
def assignments():
    faculty = get_faculty(current_user.faculty.id)
    return render_template("faculty/assignments.html", subjects=get_subjects(faculty), assignments=get_assignments(faculty))


@faculty_bp.route("/submissions")
@role_required("faculty")
def submissions():
    faculty = get_faculty(current_user.faculty.id)
    return render_template("faculty/submissions.html", submissions=get_submissions(faculty))


@faculty_bp.route("/exams")
@role_required("faculty")
def exams():
    faculty = get_faculty(current_user.faculty.id)
    return render_template("faculty/exams.html", exams=get_exams(faculty), today=date.today())


@faculty_bp.route("/notices")
@role_required("faculty")
def notices():
    return render_template("faculty/notices.html", notices=get_notices())
