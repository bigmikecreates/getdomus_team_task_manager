import pytest
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.developer import Developer
from backend.models.task import Task, TaskStatus, TaskPriority
from backend.models.task_assignment import TaskAssignment
from backend.services.dashboard_service import DashboardService


class TestDashboardService:
    async def test_stats_empty_database(self, db_session: AsyncSession):
        service = DashboardService(db_session)
        stats = await service.get_stats()

        assert stats["total_tasks"] == 0
        assert stats["by_status"] == []
        assert stats["by_priority"] == []
        assert stats["by_assignee"] == []

    async def test_stats_counts_by_status(self, db_session: AsyncSession):
        service = DashboardService(db_session)

        for status in [TaskStatus.TODO, TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE]:
            task = Task(title=f"Task {status.value}", status=status)
            db_session.add(task)
        await db_session.flush()

        stats = await service.get_stats()
        by_status = {s["status"]: s["count"] for s in stats["by_status"]}

        assert stats["total_tasks"] == 4
        assert by_status["todo"] == 2
        assert by_status["in_progress"] == 1
        assert by_status["done"] == 1

    async def test_stats_counts_by_priority(self, db_session: AsyncSession):
        service = DashboardService(db_session)

        for priority in [TaskPriority.HIGH, TaskPriority.HIGH, TaskPriority.CRITICAL]:
            task = Task(title=f"Task {priority.value}", priority=priority)
            db_session.add(task)
        await db_session.flush()

        stats = await service.get_stats()
        by_priority = {p["priority"]: p["count"] for p in stats["by_priority"]}

        assert stats["total_tasks"] == 3
        assert by_priority["high"] == 2
        assert by_priority["critical"] == 1

    async def test_stats_counts_by_assignee(self, db_session: AsyncSession):
        service = DashboardService(db_session)

        dev1 = Developer(name="Alice", email="alice@example.com", timezone="UTC")
        dev2 = Developer(name="Bob", email="bob@example.com", timezone="UTC")
        db_session.add_all([dev1, dev2])
        await db_session.flush()

        task1 = Task(title="Task 1")
        task2 = Task(title="Task 2")
        task3 = Task(title="Task 3")
        db_session.add_all([task1, task2, task3])
        await db_session.flush()

        db_session.add_all([
            TaskAssignment(task_id=task1.id, developer_id=dev1.id),
            TaskAssignment(task_id=task2.id, developer_id=dev1.id),
            TaskAssignment(task_id=task3.id, developer_id=dev2.id),
        ])
        await db_session.flush()

        stats = await service.get_stats()
        by_assignee = {a["developer_name"]: a["task_count"] for a in stats["by_assignee"]}

        assert by_assignee["Alice"] == 2
        assert by_assignee["Bob"] == 1

    async def test_overview_includes_recent_tasks(self, db_session: AsyncSession):
        service = DashboardService(db_session)

        for i in range(3):
            task = Task(title=f"Recent Task {i}")
            db_session.add(task)
        await db_session.flush()

        overview = await service.get_overview()

        assert "stats" in overview
        assert "recent_tasks" in overview
        assert len(overview["recent_tasks"]) == 3

    async def test_overview_counts_overdue_tasks(self, db_session: AsyncSession):
        service = DashboardService(db_session)

        overdue = Task(
            title="Overdue Task",
            due_date=datetime.now(timezone.utc) - timedelta(days=1),
        )
        on_time = Task(
            title="On Time Task",
            due_date=datetime.now(timezone.utc) + timedelta(days=1),
        )
        no_date = Task(title="No Due Date")
        done_overdue = Task(
            title="Done Overdue",
            status=TaskStatus.DONE,
            due_date=datetime.now(timezone.utc) - timedelta(days=1),
        )
        db_session.add_all([overdue, on_time, no_date, done_overdue])
        await db_session.flush()

        overview = await service.get_overview()

        assert overview["overdue_tasks"] == 1
