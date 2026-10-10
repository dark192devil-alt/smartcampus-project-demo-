from datetime import date

from sqlalchemy import or_

from app.extensions import db
from app.models import (
    Assignment,
    AssignmentSubmission,
    Attendance,
    Enrollment,
    Exam,
    Faculty,
    Notice,
    Student,
    Subject,
    Timetable,
)


def get_faculty(faculty_id):
    return db.session.get(Faculty, faculty_id)


def get_subjects(faculty):
    return Subject.query.filter_by(faculty_id=faculty.id).order_by(Subject.name.asc()).all()


def get_students(faculty, subject_id=None):
    subject_ids = [subject.id for subject in get_subjects(faculty)]
    selected_ids = [subject_id] if subject_id in subject_ids else subject_ids
    if not selected_ids:
        return []
    return Student.query.join(Enrollment).filter(
        Enrollment.subject_id.in_(selected_ids), Enrollment.status == "active"
    ).distinct().order_by(Student.student_number.asc()).all()


def attendance_data(faculty, subject_id=None):
    subjects = get_subjects(faculty)
    selected = next((subject for subject in subjects if subject.id == subject_id), None)
    records = Attendance.query.filter(
        Attendance.subject_id.in_([subject.id for subject in subjects])
    ).all() if subjects else []
    if selected:
        records = [record for record in records if record.subject_id == selected.id]
    students = get_students(faculty, selected.id if selected else None)
    rows = []
    for student in students:
        student_records = [record for record in records if record.student_id == student.id]
        attended = sum(record.status in {"present", "late"} for record in student_records)
        rows.append({"student": student, "attended": attended, "conducted": len(student_records)})
    attended = sum(record.status in {"present", "late"} for record in records)
    return {
        "subjects": subjects,
        "selected_subject": selected,
        "rows": rows,
        "attended": attended,
        "conducted": len(records),
        "percentage": round(attended / len(records) * 100, 1) if records else 0,
    }


def get_assignments(faculty):
    return Assignment.query.filter_by(faculty_id=faculty.id).order_by(
        Assignment.due_date.asc(), Assignment.created_at.desc()
    ).all()


def get_submissions(faculty):
    assignments = get_assignments(faculty)
    ids = [assignment.id for assignment in assignments]
    if not ids:
        return []
    return AssignmentSubmission.query.filter(
        AssignmentSubmission.assignment_id.in_(ids)
    ).order_by(AssignmentSubmission.submitted_at.desc()).all()


def get_exams(faculty):
    subject_ids = [subject.id for subject in get_subjects(faculty)]
    exams = Exam.query.filter(Exam.subject_id.in_(subject_ids)).all() if subject_ids else []
    return sorted(exams, key=lambda exam: (exam.exam_date < date.today(), exam.exam_date, exam.start_time))


def get_notices():
    return Notice.query.filter(or_(Notice.target_role == "all", Notice.target_role == "faculty")).order_by(
        Notice.published_at.desc()
    ).all()


def dashboard_data(faculty):
    subjects = get_subjects(faculty)
    timetable = Timetable.query.filter_by(faculty_id=faculty.id).order_by(
        Timetable.day.asc(), Timetable.start_time.asc()
    ).all()
    assignments = get_assignments(faculty)
    submissions = get_submissions(faculty)
    records = Attendance.query.filter(
        Attendance.subject_id.in_([subject.id for subject in subjects])
    ).all() if subjects else []
    attended = sum(record.status in {"present", "late"} for record in records)
    return {
        "subjects": subjects,
        "students": get_students(faculty),
        "today_timetable": [entry for entry in timetable if entry.day.lower() == date.today().strftime("%A").lower()],
        "attendance_percentage": round(attended / len(records) * 100, 1) if records else 0,
        "assignments": assignments,
        "pending_submissions": [submission for submission in submissions if submission.status == "submitted"],
        "exams": [exam for exam in get_exams(faculty) if exam.exam_date >= date.today()][:3],
        "notices": get_notices()[:3],
    }