from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

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
        by_status = [
            {"status": row[0].value if hasattr(row[0], "value") else row[0], "count": row[1]}
            for row in status_result.all()
        ]

        priority_result = await self.session.execute(
            select(Task.priority, func.count(Task.id)).group_by(Task.priority)
        )
        by_priority = [
            {"priority": row[0].value if hasattr(row[0], "value") else row[0], "count": row[1]}
            for row in priority_result.all()
        ]

        assignee_result = await self.session.execute(
            select(
                Developer.id,
                Developer.name,
                func.count(TaskAssignment.task_id).label("task_count"),
            )
            .join(TaskAssignment, TaskAssignment.developer_id == Developer.id)
            .group_by(Developer.id, Developer.name)
        )
        by_assignee = [
            {
                "developer_id": str(row[0]),
                "developer_name": row[1],
                "task_count": row[2],
            }
            for row in assignee_result.all()
        ]

        return {
            "total_tasks": total_tasks,
            "by_status": by_status,
            "by_priority": by_priority,
            "by_assignee": by_assignee,
        }

    async def get_overview(self) -> dict:
        stats = await self.get_stats()

        recent_result = await self.session.execute(
            select(Task)
            .order_by(Task.created_at.desc())
            .limit(5)
        )
        recent_tasks = [
            {
                "id": str(t.id),
                "title": t.title,
                "status": t.status.value if hasattr(t.status, "value") else t.status,
                "priority": t.priority.value if hasattr(t.priority, "value") else t.priority,
            }
            for t in recent_result.scalars().all()
        ]

        now = datetime.now(timezone.utc)
        overdue_result = await self.session.execute(
            select(func.count(Task.id)).where(
                Task.due_date < now,
                Task.status != TaskStatus.DONE,
            )
        )
        overdue_tasks = overdue_result.scalar()

        return {
            "stats": stats,
            "recent_tasks": recent_tasks,
            "overdue_tasks": overdue_tasks,
        }
