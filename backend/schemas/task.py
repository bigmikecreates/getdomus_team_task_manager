from datetime import datetime

from pydantic import BaseModel

from backend.models.task import TaskPriority, TaskStatus


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: datetime | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: datetime | None = None


class DeveloperSummary(BaseModel):
    id: str
    name: str
    email: str
    timezone: str

    model_config = {"from_attributes": True}


class TaskResponse(BaseModel):
    id: str
    title: str
    description: str | None = None
    status: TaskStatus
    priority: TaskPriority
    due_date: datetime | None = None
    created_by: str | None = None
    created_at: datetime
    updated_at: datetime
    developers: list[DeveloperSummary] = []

    model_config = {"from_attributes": True}


class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int


class TaskAssignmentRequest(BaseModel):
    developer_ids: list[str]
