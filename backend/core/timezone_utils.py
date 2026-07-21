"""Timezone utilities for developer availability."""

from datetime import datetime, time, timezone


def get_local_time(utc_now: datetime, tz_name: str) -> datetime:
    """Convert UTC time to local time in the given IANA timezone."""
    try:
        from zoneinfo import ZoneInfo
        local_tz = ZoneInfo(tz_name)
    except (KeyError, ValueError):
        local_tz = timezone.utc
    return utc_now.astimezone(local_tz)


def is_within_working_hours(
    now_utc: datetime,
    work_start: time | None,
    work_end: time | None,
) -> bool:
    """Check if current UTC time falls within the developer's working hours.

    Handles overnight ranges (e.g. 22:00–06:00).
    """
    if work_start is None or work_end is None:
        return False

    current_time = now_utc.time()

    if work_start <= work_end:
        return work_start <= current_time < work_end
    else:
        return current_time >= work_start or current_time < work_end


def get_timezone_offset(tz_name: str) -> str:
    """Get the current UTC offset string for a timezone."""
    try:
        from zoneinfo import ZoneInfo
        local_tz = ZoneInfo(tz_name)
    except (KeyError, ValueError):
        local_tz = timezone.utc
    now = datetime.now(timezone.utc).astimezone(local_tz)
    offset = now.utcoffset()
    total_seconds = int(offset.total_seconds())
    hours, remainder = divmod(abs(total_seconds), 3600)
    minutes = remainder // 60
    sign = "+" if total_seconds >= 0 else "-"
    return f"{sign}{hours:02d}:{minutes:02d}"


def parse_working_hours(
    start_str: str | None, end_str: str | None
) -> tuple[time | None, time | None]:
    """Parse time strings into time objects."""
    start = None
    end = None
    if start_str is not None:
        parts = start_str.split(":")
        start = time(int(parts[0]), int(parts[1]))
    if end_str is not None:
        parts = end_str.split(":")
        end = time(int(parts[0]), int(parts[1]))
    return start, end
