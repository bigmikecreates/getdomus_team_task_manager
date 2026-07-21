"""Presence service for heartbeat tracking and availability."""

from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.timezone_utils import (
    get_local_time,
    is_within_working_hours,
    get_timezone_offset,
)
from backend.repositories.developer_repository import DeveloperRepository


ONLINE_THRESHOLD_MINUTES = 5


class PresenceService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = DeveloperRepository(session)

    async def heartbeat(self, developer_id: str) -> None:
        """Update a developer's last_seen_at timestamp."""
        dev = await self.repo.get(developer_id)
        if dev is not None:
            dev.last_seen_at = datetime.now(timezone.utc)
            await self.session.flush()

    async def is_online(self, developer_id: str) -> bool:
        """Check if a developer is considered online (seen within threshold)."""
        dev = await self.repo.get(developer_id)
        if dev is None or dev.last_seen_at is None:
            return False
        threshold = datetime.now(timezone.utc) - timedelta(minutes=ONLINE_THRESHOLD_MINUTES)
        return dev.last_seen_at >= threshold

    async def get_availability(self, developer_id: str) -> dict:
        """Get full availability info for a developer."""
        dev = await self.repo.get(developer_id)
        if dev is None:
            return {"is_online": False, "is_within_working_hours": False, "local_time": ""}

        is_on = False
        if dev.last_seen_at is not None:
            threshold = datetime.now(timezone.utc) - timedelta(minutes=ONLINE_THRESHOLD_MINUTES)
            is_on = dev.last_seen_at >= threshold

        now_utc = datetime.now(timezone.utc)
        local_now = get_local_time(now_utc, dev.timezone)
        local_time_str = local_now.strftime("%H:%M")
        offset = get_timezone_offset(dev.timezone)

        within_hours = is_within_working_hours(
            now_utc, dev.working_hours_start, dev.working_hours_end
        )

        return {
            "is_online": is_on,
            "is_within_working_hours": within_hours,
            "local_time": f"{local_time_str} (UTC{offset})",
        }

    async def get_availability_bulk(self) -> dict[str, dict]:
        """Get availability for all developers at once."""
        devs = await self.repo.list_all()
        result = {}
        now_utc = datetime.now(timezone.utc)
        threshold = now_utc - timedelta(minutes=ONLINE_THRESHOLD_MINUTES)

        for dev in devs:
            is_on = dev.last_seen_at is not None and dev.last_seen_at >= threshold
            local_now = get_local_time(now_utc, dev.timezone)
            local_time_str = local_now.strftime("%H:%M")
            offset = get_timezone_offset(dev.timezone)
            within_hours = is_within_working_hours(
                now_utc, dev.working_hours_start, dev.working_hours_end
            )
            result[dev.id] = {
                "is_online": is_on,
                "is_within_working_hours": within_hours,
                "local_time": f"{local_time_str} (UTC{offset})",
            }
        return result
