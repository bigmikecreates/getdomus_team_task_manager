from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.core.dependencies import get_current_user, require_role
from backend.models.user import User
from backend.schemas.developer import DeveloperCreate, DeveloperUpdate, DeveloperResponse
from backend.services.developer_service import DeveloperService

router = APIRouter(prefix="/api/developers", tags=["developers"])


@router.get("", response_model=list[DeveloperResponse])
async def list_developers(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = DeveloperService(db)
    return await service.list_developers()


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
