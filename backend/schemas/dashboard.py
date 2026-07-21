from datetime import datetime

from pydantic import BaseModel


class StatusCount(BaseModel):
    status: str
    count: int


class PriorityCount(BaseModel):
    priority: str
    count: int


class AssigneeCount(BaseModel):
    developer_id: str
    developer_name: str
    task_count: int


class DashboardStats(BaseModel):
    total_tasks: int
    by_status: list[StatusCount]
    by_priority: list[PriorityCount]
    by_assignee: list[AssigneeCount]


class UpcomingTask(BaseModel):
    id: str
    title: str
    status: str
    priority: str
    due_date: datetime | None = None


class DashboardOverview(BaseModel):
    stats: DashboardStats
    overdue_tasks: int
    critical_tasks: int
    upcoming_tasks: list[UpcomingTask]
    recent_tasks: list[dict]
