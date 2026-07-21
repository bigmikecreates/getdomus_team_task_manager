"""Task business logic — creation, queries, and developer assignments.

Coordinates TaskRepository for CRUD and TaskAssignment rows for the
many-to-many developer ↔ task link. All methods share the caller's
AsyncSession so they participate in the same transaction.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.developer import Developer
from backend.models.task import Task, TaskStatus, TaskPriority
from backend.models.task_assignment import TaskAssignment
from backend.repositories.task_repository import TaskRepository


class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = TaskRepository(session)

    async def create_task(self, title: str, description: str | None = None, status: TaskStatus = TaskStatus.TODO, priority: TaskPriority = TaskPriority.MEDIUM, due_date=None) -> Task:
        task = await self.repo.create(
            title=title,
            description=description,
            status=status,
            priority=priority,
            due_date=due_date,
        )
        return await self.get_task(task.id)

    async def get_task(self, task_id: str) -> Task | None:
        result = await self.session.execute(
            select(Task)
            .where(Task.id == task_id)
            .execution_options(populate_existing=True)
        )
        return result.scalar_one_or_none()

    async def list_tasks(self) -> list[Task]:
        result = await self.session.execute(
            select(Task).execution_options(populate_existing=True)
        )
        return list(result.scalars().all())

    async def update_task(self, task_id: str, **kwargs) -> Task | None:
        return await self.repo.update(task_id, **kwargs)

    async def assign_developer(self, task_id: str, developer_id: str) -> bool:
        existing = await self.session.execute(
            select(TaskAssignment).where(
                TaskAssignment.task_id == task_id,
                TaskAssignment.developer_id == developer_id,
            )
        )
        if existing.scalar_one_or_none() is not None:
            raise ValueError("Developer already assigned to this task")

        assignment = TaskAssignment(task_id=task_id, developer_id=developer_id)
        self.session.add(assignment)
        await self.session.flush()
        return True

    async def unassign_developer(self, task_id: str, developer_id: str) -> bool:
        result = await self.session.execute(
            select(TaskAssignment).where(
                TaskAssignment.task_id == task_id,
                TaskAssignment.developer_id == developer_id,
            )
        )
        assignment = result.scalar_one_or_none()
        if assignment is None:
            return False
        await self.session.delete(assignment)
        await self.session.flush()
        return True
