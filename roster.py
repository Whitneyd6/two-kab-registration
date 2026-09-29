"""Student A - Roster & Check-In Module.

Handles student profiles and daily check-ins, stored in attendance_log.json.

File layout:
{
  "students": {"S001": {"name": "Amina K", "student_id": "S001"}},
  "records":  [{"student_id": "S001", "date": "2026-09-29",
                "status": "Present", "timestamp": "2026-09-29 08:05:12"}]
}
"""
import json
import os
from datetime import datetime

LOG_FILE = "attendance_log.json"
CHECK_IN_STATUSES = ("Present", "Late")


# ---------- persistence ----------
def load_data():
    """Read the JSON file; return an empty structure if missing or corrupt."""
    if not os.path.exists(LOG_FILE):
        return {"students": {}, "records": []}
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"students": {}, "records": []}
    data.setdefault("students", {})
    data.setdefault("records", [])
    return data


def save_data(data):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ---------- core logic ----------
def create_student(name, student_id):
    """Create a profile. Returns (ok, message)."""
    name, student_id = name.strip(), student_id.strip().upper()
    if not name or not student_id:
        return False, "Name and Student ID are required."
    data = load_data()
    if student_id in data["students"]:
        return False, f"Student ID {student_id} already exists."
    data["students"][student_id] = {"name": name, "student_id": student_id}
    save_data(data)
    return True, f"Student {name} ({student_id}) created."


def check_in(student_id, status, date=None):
    """Log 'Present' or 'Late' with a timestamp.

    If the student already has a record for that date (e.g. a previous
    check-in, or an 'Absent' flag from the reporting module), it is
    UPDATED instead of duplicated. Returns (ok, message).
    """
    student_id = student_id.strip().upper()
    status = status.strip().capitalize()
    if status not in CHECK_IN_STATUSES:
        return False, "Status must be 'Present' or 'Late'."

    data = load_data()
    if student_id not in data["students"]:
        return False, f"Unknown student ID {student_id}."

    now = datetime.now()
    date = date or now.strftime("%Y-%m-%d")
    stamp = now.strftime("%Y-%m-%d %H:%M:%S")

    for rec in data["records"]:
        if rec["student_id"] == student_id and rec["date"] == date:
            rec["status"], rec["timestamp"] = status, stamp
            save_data(data)
            return True, f"Updated {student_id} to {status} for {date}."

    data["records"].append({"student_id": student_id, "date": date,
                            "status": status, "timestamp": stamp})
    save_data(data)
    return True, f"{student_id} checked in as {status} on {date}."


def students_checked_in_today():
    """Return list of (student_id, name, status, timestamp) for today."""
    data = load_data()
    today = datetime.now().strftime("%Y-%m-%d")
    rows = []
    for rec in data["records"]:
        if rec["date"] == today and rec["status"] in CHECK_IN_STATUSES:
            name = data["students"].get(rec["student_id"], {}).get("name", "?")
            rows.append((rec["student_id"], name, rec["status"], rec["timestamp"]))
    return sorted(rows, key=lambda r: r[3])


# ---------- CLI handlers (called from app.py) ----------
def menu_create_student():
    name = input("Student name: ")
    sid = input("Student ID: ")
    print(create_student(name, sid)[1])


def menu_check_in():
    sid = input("Student ID: ")
    status = input("Status (Present/Late): ")
    print(check_in(sid, status)[1])


def menu_today_summary():
    rows = students_checked_in_today()
    if not rows:
        print("No students checked in today.")
        return
    print(f"\nChecked in today ({len(rows)}):")
    for sid, name, status, stamp in rows:
        print(f"  {sid:<8} {name:<20} {status:<8} {stamp[11:]}")
