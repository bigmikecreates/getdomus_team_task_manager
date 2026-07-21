import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models.developer import Developer
from backend.models.task import Task, TaskPriority, TaskStatus
from backend.models.task_assignment import TaskAssignment
from backend.models.user import User, UserRole


class TestDeveloperModel:
    async def test_developer_has_required_fields(self, db_session: AsyncSession):
        developer = Developer(
            name="Jane Smith",
            email="jane@example.com",
            timezone="Europe/London",
        )
        db_session.add(developer)
        await db_session.flush()

        assert developer.id is not None
        assert developer.name == "Jane Smith"
        assert developer.email == "jane@example.com"
        assert developer.timezone == "Europe/London"
        assert developer.created_at is not None
        assert developer.updated_at is not None

    async def test_developer_email_is_unique(self, db_session: AsyncSession):
        dev1 = Developer(name="Dev 1", email="same@example.com", timezone="UTC")
        dev2 = Developer(name="Dev 2", email="same@example.com", timezone="UTC")
        db_session.add(dev1)
        db_session.flush()

        with pytest.raises(Exception):
            db_session.add(dev2)
            await db_session.flush()

    async def test_developer_defaults_to_utc_timezone(self, db_session: AsyncSession):
        developer = Developer(name="No TZ Dev", email="notz@example.com")
        db_session.add(developer)
        await db_session.flush()

        assert developer.timezone == "UTC"

    async def test_developer_optional_working_hours(self, db_session: AsyncSession):
        developer = Developer(
            name="Working Hours Dev",
            email="hours@example.com",
            timezone="America/New_York",
        )
        db_session.add(developer)
        await db_session.flush()

        assert developer.working_hours_start is None
        assert developer.working_hours_end is None


class TestUserModel:
    async def test_user_has_required_fields(self, db_session: AsyncSession):
        user = User(
            email="test@example.com",
            password_hash="hashedpassword123",
            role=UserRole.DEVELOPER,
        )
        db_session.add(user)
        await db_session.flush()

        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.password_hash == "hashedpassword123"
        assert user.role == UserRole.DEVELOPER
        assert user.created_at is not None

    async def test_user_email_is_unique(self, db_session: AsyncSession):
        user1 = User(email="dup@example.com", password_hash="hash1", role=UserRole.DEVELOPER)
        user2 = User(email="dup@example.com", password_hash="hash2", role=UserRole.DEVELOPER)
        db_session.add(user1)
        db_session.flush()

        with pytest.raises(Exception):
            db_session.add(user2)
            await db_session.flush()

    async def test_user_defaults_to_developer_role(self, db_session: AsyncSession):
        user = User(email="default@example.com", password_hash="hash")
        db_session.add(user)
        await db_session.flush()

        assert user.role == UserRole.DEVELOPER

    async def test_user_optional_developer_link(self, db_session: AsyncSession):
        user = User(email="nolink@example.com", password_hash="hash")
        db_session.add(user)
        await db_session.flush()

        assert user.developer_id is None


class TestTaskModel:
    async def test_task_has_required_fields(self, db_session: AsyncSession):
        task = Task(
            title="Test Task",
            description="A test description",
            status=TaskStatus.TODO,
            priority=TaskPriority.HIGH,
        )
        db_session.add(task)
        await db_session.flush()

        assert task.id is not None
        assert task.title == "Test Task"
        assert task.description == "A test description"
        assert task.status == TaskStatus.TODO
        assert task.priority == TaskPriority.HIGH
        assert task.created_at is not None
        assert task.updated_at is not None

    async def test_task_status_defaults_to_todo(self, db_session: AsyncSession):
        task = Task(title="Default Status Task")
        db_session.add(task)
        await db_session.flush()

        assert task.status == TaskStatus.TODO

    async def test_task_priority_defaults_to_medium(self, db_session: AsyncSession):
        task = Task(title="Default Priority Task")
        db_session.add(task)
        await db_session.flush()

        assert task.priority == TaskPriority.MEDIUM

    async def test_task_optional_fields(self, db_session: AsyncSession):
        task = Task(title="Minimal Task")
        db_session.add(task)
        await db_session.flush()

        assert task.description is None
        assert task.due_date is None
        assert task.created_by is None

    async def test_task_has_many_developers(self, db_session: AsyncSession):
        task = Task(title="Multi Dev Task")
        dev1 = Developer(name="Dev 1", email="dev1@example.com")
        dev2 = Developer(name="Dev 2", email="dev2@example.com")
        db_session.add_all([task, dev1, dev2])
        await db_session.flush()

        assignment1 = TaskAssignment(task_id=task.id, developer_id=dev1.id)
        assignment2 = TaskAssignment(task_id=task.id, developer_id=dev2.id)
        db_session.add_all([assignment1, assignment2])
        await db_session.flush()

        result = await db_session.execute(
            select(Task)
            .where(Task.id == task.id)
            .options(selectinload(Task.developers))
        )
        loaded_task = result.scalar_one()
        assert len(loaded_task.developers) == 2


class TestTaskAssignmentModel:
    async def test_taskassignment_composite_key(self, db_session: AsyncSession):
        task = Task(title="Assignment Task")
        developer = Developer(name="Assigned Dev", email="assigned@example.com")
        db_session.add_all([task, developer])
        await db_session.flush()

        assignment = TaskAssignment(task_id=task.id, developer_id=developer.id)
        db_session.add(assignment)
        await db_session.flush()

        assert assignment.task_id == task.id
        assert assignment.developer_id == developer.id
        assert assignment.assigned_at is not None

    async def test_taskassignment_duplicate_raises(self, db_session: AsyncSession):
        task = Task(title="Dup Assignment Task")
        developer = Developer(name="Dup Dev", email="dup@example.com")
        db_session.add_all([task, developer])
        await db_session.flush()

        assignment1 = TaskAssignment(task_id=task.id, developer_id=developer.id)
        db_session.add(assignment1)
        await db_session.flush()

        assignment2 = TaskAssignment(task_id=task.id, developer_id=developer.id)
        with pytest.raises(Exception):
            db_session.add(assignment2)
            await db_session.flush()
