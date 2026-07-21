from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models.developer import Developer
from backend.models.task import Task, TaskStatus, TaskPriority
from backend.models.task_assignment import TaskAssignment


class DashboardService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_stats(self) -> dict:
        total_result = await self.session.execute(select(func.count(Task.id)))
        total_tasks = total_result.scalar()

        status_result = await self.session.execute(
            select(Task.status, func.count(Task.id)).group_by(Task.status)
        )
        by_status = [{"status": row[0].value if hasattr(row[0], 'value') else row[0], "count": row[1]} for row in status_result.all()]

        priority_result = await self.session.execute(
            select(Task.priority, func.count(Task.id)).group_by(Task.priority)
        )
        by_priority = [{"priority": row[0].value if hasattr(row[0], 'value') else row[0], "count": row[1]} for row in priority_result.all()]

        return {
            "total_tasks": total_tasks,
            "by_status": by_status,
            "by_priority": by_priority,
        }

    async def get_overview(self) -> dict:
        stats = await self.get_stats()
        return {
            "stats": stats,
            "recent_tasks": [],
            "overdue_tasks": 0,
        }
