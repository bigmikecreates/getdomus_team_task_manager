"""Tests for timezone utilities and presence logic."""

from datetime import datetime, time, timezone, timedelta

import pytest

from backend.core.timezone_utils import (
    get_local_time,
    is_within_working_hours,
    get_timezone_offset,
    parse_working_hours,
)


class TestGetLocalTime:
    def test_utc_unchanged(self):
        utc_time = datetime(2026, 7, 15, 14, 30, 0, tzinfo=timezone.utc)
        local = get_local_time(utc_time, "UTC")
        assert local.hour == 14
        assert local.minute == 30
        assert str(local.tzinfo) == "UTC"

    def test_new_york_shift(self):
        utc_time = datetime(2026, 7, 15, 14, 30, 0, tzinfo=timezone.utc)
        local = get_local_time(utc_time, "America/New_York")
        assert local.hour == 10
        assert local.minute == 30

    def test_tokyo_shift(self):
        utc_time = datetime(2026, 7, 15, 14, 30, 0, tzinfo=timezone.utc)
        local = get_local_time(utc_time, "Asia/Tokyo")
        assert local.hour == 23
        assert local.minute == 30

    def test_invalid_timezone_returns_utc(self):
        utc_time = datetime(2026, 7, 15, 14, 30, 0, tzinfo=timezone.utc)
        local = get_local_time(utc_time, "Invalid/Zone")
        assert local.hour == 14
        assert str(local.tzinfo) == "UTC"


class TestIsWithinWorkingHours:
    def test_within_standard_hours(self):
        now = datetime(2026, 7, 15, 10, 0, 0, tzinfo=timezone.utc)
        result = is_within_working_hours(now, time(9, 0), time(17, 0))
        assert result is True

    def test_outside_standard_hours(self):
        now = datetime(2026, 7, 15, 18, 0, 0, tzinfo=timezone.utc)
        result = is_within_working_hours(now, time(9, 0), time(17, 0))
        assert result is False

    def test_no_working_hours_returns_false(self):
        now = datetime(2026, 7, 15, 10, 0, 0, tzinfo=timezone.utc)
        result = is_within_working_hours(now, None, None)
        assert result is False

    def test_overnight_hours(self):
        # Worker with hours 22:00-06:00 (night shift)
        now = datetime(2026, 7, 15, 23, 0, 0, tzinfo=timezone.utc)
        result = is_within_working_hours(now, time(22, 0), time(6, 0))
        assert result is True

    def test_overnight_hours_outside(self):
        now = datetime(2026, 7, 15, 12, 0, 0, tzinfo=timezone.utc)
        result = is_within_working_hours(now, time(22, 0), time(6, 0))
        assert result is False

    def test_boundary_exact_start(self):
        now = datetime(2026, 7, 15, 9, 0, 0, tzinfo=timezone.utc)
        result = is_within_working_hours(now, time(9, 0), time(17, 0))
        assert result is True

    def test_boundary_exact_end(self):
        now = datetime(2026, 7, 15, 17, 0, 0, tzinfo=timezone.utc)
        result = is_within_working_hours(now, time(9, 0), time(17, 0))
        assert result is False


class TestGetTimezoneOffset:
    def test_utc_offset_zero(self):
        offset = get_timezone_offset("UTC")
        assert offset == "+00:00"

    def test_new_york_offset(self):
        offset = get_timezone_offset("America/New_York")
        # EST is -05:00, EDT is -04:00 (July is DST)
        assert offset in ("-04:00", "-05:00")

    def test_tokyo_offset(self):
        offset = get_timezone_offset("Asia/Tokyo")
        assert offset == "+09:00"

    def test_invalid_timezone_returns_utc(self):
        offset = get_timezone_offset("Invalid/Zone")
        assert offset == "+00:00"


class TestParseWorkingHours:
    def test_parse_valid(self):
        start, end = parse_working_hours("09:00", "17:00")
        assert start == time(9, 0)
        assert end == time(17, 0)

    def test_parse_none(self):
        start, end = parse_working_hours(None, None)
        assert start is None
        assert end is None

    def test_parse_partial(self):
        start, end = parse_working_hours("09:00", None)
        assert start == time(9, 0)
        assert end is None
