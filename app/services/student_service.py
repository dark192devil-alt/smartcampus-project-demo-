from datetime import date, datetime

from sqlalchemy import or_

from app.extensions import db
from app.models import (
    Assignment,
    AssignmentSubmission,
    Attendance,
    Event,
    Exam,
    Notice,
    Student,
    Subject,
    Timetable,
)


def get_student(student_id):
    return db.session.get(Student, student_id)


def get_enrolled_subject_ids(student):
    return [enrollment.subject_id for enrollment in student.enrollments if enrollment.status == "active"]


def _attendance_summary(records):
    conducted = len(records)
    attended = sum(record.status in {"present", "late"} for record in records)
    percentage = round((attended / conducted) * 100, 1) if conducted else 0
    return {
        "attended": attended,
        "conducted": conducted,
        "percentage": percentage,
    }


def get_attendance_data(student):
    subjects = [enrollment.subject for enrollment in student.enrollments if enrollment.status == "active"]
    records = Attendance.query.filter_by(student_id=student.id).all()
    by_subject = []
    for subject in subjects:
        subject_records = [record for record in records if record.subject_id == subject.id]
        summary = _attendance_summary(subject_records)
        by_subject.append({"subject": subject, **summary})

    overall = _attendance_summary(records)
    return {"overall": overall, "by_subject": by_subject, "has_records": bool(records)}


def get_assignments(student, subject_id=None, status=None):
    subject_ids = get_enrolled_subject_ids(student)
    assignments = Assignment.query.filter(Assignment.subject_id.in_(subject_ids)).order_by(
        Assignment.due_date.asc(), Assignment.created_at.desc()
    ).all() if subject_ids else []

    submissions = {
        submission.assignment_id: submission
        for submission in AssignmentSubmission.query.filter_by(student_id=student.id).all()
    }
    items = []
    today = date.today()
    for assignment in assignments:
        submission = submissions.get(assignment.id)
        if submission:
            item_status = "late" if submission.status == "late" or submission.submitted_at.date() > assignment.due_date else "submitted"
        else:
            item_status = "pending"
        if subject_id and assignment.subject_id != subject_id:
            continue
        if status and item_status != status:
            continue
        items.append({
            "assignment": assignment,
            "submission": submission,
            "status": item_status,
            "is_overdue": item_status == "pending" and assignment.due_date < today,
        })
    return items


def get_exams(student):
    subject_ids = get_enrolled_subject_ids(student)
    exams = Exam.query.filter(
        Exam.course_id == student.course_id,
        Exam.subject_id.in_(subject_ids),
    ).all() if subject_ids else []
    today = date.today()
    items = [{"exam": exam, "is_upcoming": exam.exam_date >= today} for exam in exams]
    return sorted(items, key=lambda item: (not item["is_upcoming"], item["exam"].exam_date, item["exam"].start_time))


def get_timetable(student):
    subject_ids = get_enrolled_subject_ids(student)
    if not subject_ids:
        return []
    return Timetable.query.filter(
        Timetable.course_id == student.course_id,
        Timetable.subject_id.in_(subject_ids),
    ).order_by(Timetable.day.asc(), Timetable.start_time.asc()).all()


def get_notices(limit=None):
    query = Notice.query.filter(or_(Notice.target_role == "all", Notice.target_role == "student")).order_by(
        Notice.published_at.desc()
    )
    if limit:
        query = query.limit(limit)
    notices = query.all()
    return [
        {
            "notice": notice,
            "category": "Academic" if notice.target_role == "student" else "College",
            "priority": "Important" if notice.summary else "General",
        }
        for notice in notices
    ]


def get_events(limit=None):
    query = Event.query.filter(Event.event_date >= datetime.now()).order_by(Event.event_date.asc())
    if limit:
        query = query.limit(limit)
    return query.all()


def get_dashboard_data(student):
    attendance = get_attendance_data(student)
    assignments = get_assignments(student)
    exams = get_exams(student)
    timetable = get_timetable(student)
    today_name = date.today().strftime("%A")
    today_timetable = [entry for entry in timetable if entry.day.lower() == today_name.lower()]
    return {
        "attendance": attendance,
        "assignments": assignments,
        "pending_assignments": [item for item in assignments if item["status"] == "pending"],
        "exams": [item for item in exams if item["is_upcoming"]][:3],
        "events": get_events(limit=3),
        "notices": get_notices(limit=3),
        "today_timetable": today_timetable,
    }