import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.developer import Developer
from backend.models.task import Task, TaskPriority, TaskStatus
from backend.repositories.task_repository import TaskRepository


class TestTaskRepository:
    async def test_create_task(self, db_session: AsyncSession):
        repo = TaskRepository(db_session)
        task = await repo.create(
            title="New Task",
            description="Task description",
            status=TaskStatus.TODO,
            priority=TaskPriority.HIGH,
        )

        assert task.id is not None
        assert task.title == "New Task"
        assert task.description == "Task description"
        assert task.status == TaskStatus.TODO
        assert task.priority == TaskPriority.HIGH

    async def test_get_task_by_id(self, db_session: AsyncSession):
        repo = TaskRepository(db_session)
        task = await repo.create(title="Get Me Task")
        found = await repo.get(task.id)

        assert found is not None
        assert found.id == task.id
        assert found.title == "Get Me Task"

    async def test_get_nonexistent_task_returns_none(self, db_session: AsyncSession):
        repo = TaskRepository(db_session)
        found = await repo.get("nonexistent-id")

        assert found is None

    async def test_list_all_tasks(self, db_session: AsyncSession):
        repo = TaskRepository(db_session)
        await repo.create(title="Task 1")
        await repo.create(title="Task 2")
        await repo.create(title="Task 3")

        tasks = await repo.list_all()

        assert len(tasks) == 3

    async def test_list_tasks_by_status(self, db_session: AsyncSession):
        repo = TaskRepository(db_session)
        await repo.create(title="Todo Task", status=TaskStatus.TODO)
        await repo.create(title="Done Task", status=TaskStatus.DONE)

        todo_tasks = await repo.list_by_status(TaskStatus.TODO)

        assert len(todo_tasks) == 1
        assert todo_tasks[0].title == "Todo Task"

    async def test_update_task(self, db_session: AsyncSession):
        repo = TaskRepository(db_session)
        task = await repo.create(title="Original Title")

        updated = await repo.update(task.id, title="Updated Title", priority=TaskPriority.CRITICAL)

        assert updated is not None
        assert updated.title == "Updated Title"
        assert updated.priority == TaskPriority.CRITICAL

    async def test_update_nonexistent_task_returns_none(self, db_session: AsyncSession):
        repo = TaskRepository(db_session)
        updated = await repo.update("nonexistent-id", title="Nope")

        assert updated is None

    async def test_delete_task(self, db_session: AsyncSession):
        repo = TaskRepository(db_session)
        task = await repo.create(title="Delete Me")

        result = await repo.delete(task.id)

        assert result is True
        found = await repo.get(task.id)
        assert found is None

    async def test_delete_nonexistent_task_returns_false(self, db_session: AsyncSession):
        repo = TaskRepository(db_session)
        result = await repo.delete("nonexistent-id")

        assert result is False
