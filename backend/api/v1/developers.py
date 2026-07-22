from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.core.dependencies import get_current_user, require_role
from backend.models.user import User
from backend.schemas.developer import DeveloperCreate, DeveloperUpdate, DeveloperResponse, DeveloperWithAvailability
from backend.services.developer_service import DeveloperService
from backend.services.presence_service import PresenceService

router = APIRouter(prefix="/api/developers", tags=["developers"])


@router.get("", response_model=list[DeveloperWithAvailability])
async def list_developers(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = DeveloperService(db)
    devs = await service.list_developers()
    presence = PresenceService(db)
    availability = await presence.get_availability_bulk()
    result = []
    for dev in devs:
        avail = availability.get(dev.id, {})
        result.append(DeveloperWithAvailability(
            id=dev.id,
            name=dev.name,
            email=dev.email,
            timezone=dev.timezone,
            working_hours_start=dev.working_hours_start,
            working_hours_end=dev.working_hours_end,
            created_at=dev.created_at,
            updated_at=dev.updated_at,
            is_online=avail.get("is_online", False),
            is_within_working_hours=avail.get("is_within_working_hours", False),
            local_time=avail.get("local_time", ""),
        ))
    return result


@router.post("", response_model=DeveloperResponse, status_code=status.HTTP_201_CREATED)
async def create_developer(
    request: DeveloperCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    service = DeveloperService(db)
    return await service.create_developer(
        name=request.name,
        email=request.email,
        timezone=request.timezone,
        working_hours_start=request.working_hours_start,
        working_hours_end=request.working_hours_end,
    )


@router.put("/{developer_id}", response_model=DeveloperResponse)
async def update_developer(
    developer_id: str,
    request: DeveloperUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    service = DeveloperService(db)
    developer = await service.update_developer(
        developer_id,
        name=request.name,
        email=request.email,
        timezone=request.timezone,
        working_hours_start=request.working_hours_start,
        working_hours_end=request.working_hours_end,
    )
    if developer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Developer not found")
    return developer


@router.delete("/{developer_id}")
async def delete_developer(
    developer_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    service = DeveloperService(db)
    result = await service.delete_developer(developer_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Developer not found")
    return {"message": "Developer deleted successfully"}
