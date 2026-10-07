"""Attendance ingestion is paused until member-by-meeting parsing is validated."""


def scrape_attendance_notices():
    # An unavailable source cannot produce mock notices.
    return []
