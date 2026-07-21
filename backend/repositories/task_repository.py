from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.task import Task, TaskStatus


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, title: str, description: str | None = None, status: TaskStatus = TaskStatus.TODO, **kwargs) -> Task:
        task = Task(title=title, description=description, status=status, **kwargs)
        self.session.add(task)
        await self.session.flush()
        return task

    async def get(self, task_id: str) -> Task | None:
        result = await self.session.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()

    async def list_all(self) -> list[Task]:
        result = await self.session.execute(select(Task))
        return list(result.scalars().all())

    async def list_by_status(self, status: TaskStatus) -> list[Task]:
        result = await self.session.execute(select(Task).where(Task.status == status))
        return list(result.scalars().all())

    async def update(self, task_id: str, **kwargs) -> Task | None:
        task = await self.get(task_id)
        if task is None:
            return None
        for key, value in kwargs.items():
            if value is not None:
                setattr(task, key, value)
        await self.session.flush()
        return task
