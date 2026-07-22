"""Heartbeat endpoint for presence tracking."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.core.dependencies import get_current_user
from backend.models.user import User
from backend.services.presence_service import PresenceService

router = APIRouter(prefix="/api/presence", tags=["presence"])


@router.post("/heartbeat")
async def heartbeat(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Record a heartbeat for the current user's linked developer, if any."""
    if current_user.developer_id:
        service = PresenceService(db)
        await service.heartbeat(current_user.developer_id)
    return {"status": "ok"}
