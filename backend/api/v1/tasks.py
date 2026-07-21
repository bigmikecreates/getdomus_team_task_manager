from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.core.dependencies import get_current_user, require_role
from backend.models.user import User
from backend.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse, TaskAssignmentRequest
from backend.services.task_service import TaskService

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    tasks = await service.list_tasks()
    return TaskListResponse(tasks=tasks, total=len(tasks))


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin", "manager")),
):
    service = TaskService(db)
    task = await service.create_task(
        title=request.title,
        description=request.description,
        status=request.status,
        priority=request.priority,
        due_date=request.due_date,
    )
    return task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    task = await service.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    request: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin", "manager")),
):
    service = TaskService(db)
    task = await service.update_task(
        task_id,
        title=request.title,
        description=request.description,
        status=request.status,
        priority=request.priority,
        due_date=request.due_date,
    )
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.post("/{task_id}/assign")
async def assign_developer(
    task_id: str,
    request: TaskAssignmentRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin", "manager")),
):
    service = TaskService(db)
    for developer_id in request.developer_ids:
        try:
            await service.assign_developer(task_id, developer_id)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"message": "Developers assigned successfully"}


@router.delete("/{task_id}/assignments/{developer_id}")
async def unassign_developer(
    task_id: str,
    developer_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin", "manager")),
):
    service = TaskService(db)
    result = await service.unassign_developer(task_id, developer_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
    return {"message": "Developer unassigned successfully"}
