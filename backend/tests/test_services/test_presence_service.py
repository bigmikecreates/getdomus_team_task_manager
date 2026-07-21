"""Tests for presence service (heartbeat + online status)."""

from datetime import datetime, time, timedelta, timezone
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.developer import Developer
from backend.services.presence_service import PresenceService
from backend.core.timezone_utils import get_local_time, is_within_working_hours


class TestPresenceService:
    async def test_heartbeat_updates_last_seen(self, db_session: AsyncSession):
        dev = Developer(
            name="Online Dev",
            email="online@example.com",
            timezone="UTC",
        )
        db_session.add(dev)
        await db_session.flush()

        service = PresenceService(db_session)
        await service.heartbeat(dev.id)

        await db_session.refresh(dev)
        assert dev.last_seen_at is not None

    async def test_heartbeat_nonexistent_dev_no_error(self, db_session: AsyncSession):
        service = PresenceService(db_session)
        await service.heartbeat("nonexistent-id")

    async def test_is_online_recent_heartbeat(self, db_session: AsyncSession):
        dev = Developer(
            name="Recently Active",
            email="recent@example.com",
            timezone="UTC",
            last_seen_at=datetime.now(timezone.utc) - timedelta(minutes=1),
        )
        db_session.add(dev)
        await db_session.flush()

        service = PresenceService(db_session)
        assert await service.is_online(dev.id) is True

    async def test_is_online_stale_heartbeat(self, db_session: AsyncSession):
        dev = Developer(
            name="Stale Dev",
            email="stale@example.com",
            timezone="UTC",
            last_seen_at=datetime.now(timezone.utc) - timedelta(minutes=10),
        )
        db_session.add(dev)
        await db_session.flush()

        service = PresenceService(db_session)
        assert await service.is_online(dev.id) is False

    async def test_is_online_never_seen(self, db_session: AsyncSession):
        dev = Developer(
            name="Never Seen",
            email="never@example.com",
            timezone="UTC",
            last_seen_at=None,
        )
        db_session.add(dev)
        await db_session.flush()

        service = PresenceService(db_session)
        assert await service.is_online(dev.id) is False

    async def test_get_developer_availability(self, db_session: AsyncSession):
        dev = Developer(
            name="Available Dev",
            email="available@example.com",
            timezone="UTC",
            working_hours_start=time(9, 0),
            working_hours_end=time(17, 0),
            last_seen_at=datetime.now(timezone.utc) - timedelta(minutes=1),
        )
        db_session.add(dev)
        await db_session.flush()

        service = PresenceService(db_session)
        result = await service.get_availability(dev.id)

        assert result["is_online"] is True
        assert "is_within_working_hours" in result
        assert "local_time" in result
        assert result["local_time"] != ""
