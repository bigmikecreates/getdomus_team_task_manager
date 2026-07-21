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


class DashboardOverview(BaseModel):
    stats: DashboardStats
    recent_tasks: list[dict]
    overdue_tasks: int
