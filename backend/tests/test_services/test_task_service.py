import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.developer import Developer
from backend.models.task import Task, TaskPriority, TaskStatus
from backend.models.user import User, UserRole
from backend.services.task_service import TaskService
from backend.core.security import hash_password


class TestTaskService:
    async def test_create_task(self, db_session: AsyncSession):
        service = TaskService(db_session)
        task = await service.create_task(
            title="Service Task",
            description="Created via service",
            priority=TaskPriority.HIGH,
        )

        assert task.id is not None
        assert task.title == "Service Task"

    async def test_assign_developer_to_task(self, db_session: AsyncSession):
        service = TaskService(db_session)
        task = await service.create_task(title="Assign Task")
        developer = Developer(name="Assign Dev", email="assign@example.com", timezone="UTC")
        db_session.add(developer)
        await db_session.flush()

        result = await service.assign_developer(task.id, developer.id)

        assert result is True

    async def test_assign_duplicate_developer_raises(self, db_session: AsyncSession):
        service = TaskService(db_session)
        task = await service.create_task(title="Dup Assign Task")
        developer = Developer(name="Dup Dev", email="dup@example.com", timezone="UTC")
        db_session.add(developer)
        await db_session.flush()

        await service.assign_developer(task.id, developer.id)

        with pytest.raises(ValueError, match="already assigned"):
            await service.assign_developer(task.id, developer.id)

    async def test_unassign_developer(self, db_session: AsyncSession):
        service = TaskService(db_session)
        task = await service.create_task(title="Unassign Task")
        developer = Developer(name="Unassign Dev", email="unassign@example.com", timezone="UTC")
        db_session.add(developer)
        await db_session.flush()

        await service.assign_developer(task.id, developer.id)
        result = await service.unassign_developer(task.id, developer.id)

        assert result is True

    async def test_update_task(self, db_session: AsyncSession):
        service = TaskService(db_session)
        task = await service.create_task(title="Original")

        updated = await service.update_task(task.id, title="Updated", status=TaskStatus.IN_PROGRESS)

        assert updated is not None
        assert updated.title == "Updated"
        assert updated.status == TaskStatus.IN_PROGRESS

    async def test_get_task_with_developers(self, db_session: AsyncSession):
        service = TaskService(db_session)
        task = await service.create_task(title="With Devs")
        developer = Developer(name="Dev", email="dev@example.com", timezone="UTC")
        db_session.add(developer)
        await db_session.flush()

        await service.assign_developer(task.id, developer.id)
        result = await service.get_task(task.id)

        assert result is not None
        assert len(result.developers) == 1

    async def test_delete_task(self, db_session: AsyncSession):
        service = TaskService(db_session)
        task = await service.create_task(title="Delete Me")

        result = await service.delete_task(task.id)

        assert result is True
        found = await service.get_task(task.id)
        assert found is None

    async def test_delete_nonexistent_task_returns_false(self, db_session: AsyncSession):
        service = TaskService(db_session)
        result = await service.delete_task("nonexistent-id")

        assert result is False

    async def test_delete_task_with_assignments(self, db_session: AsyncSession):
        service = TaskService(db_session)
        task = await service.create_task(title="Delete With Devs")
        developer = Developer(name="Del Dev", email="deldev@example.com", timezone="UTC")
        db_session.add(developer)
        await db_session.flush()

        await service.assign_developer(task.id, developer.id)
        result = await service.delete_task(task.id)

        assert result is True
