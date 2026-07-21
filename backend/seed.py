import asyncio
from datetime import datetime, time, timezone, timedelta

from backend.core.database import async_session_factory
from backend.core.security import hash_password
from backend.models.developer import Developer
from backend.models.task import Task, TaskStatus, TaskPriority
from backend.models.task_assignment import TaskAssignment
from backend.repositories.developer_repository import DeveloperRepository
from backend.repositories.user_repository import UserRepository
from backend.repositories.task_repository import TaskRepository

DEVELOPERS = [
    {"name": "Alice Chen", "email": "alice@example.com", "timezone": "America/New_York", "working_hours_start": time(9, 0), "working_hours_end": time(17, 0)},
    {"name": "Bob Kumar", "email": "bob@example.com", "timezone": "Europe/London", "working_hours_start": time(8, 0), "working_hours_end": time(16, 0)},
    {"name": "Carla Rossi", "email": "carla@example.com", "timezone": "Asia/Tokyo", "working_hours_start": time(10, 0), "working_hours_end": time(18, 0)},
    {"name": "David Okafor", "email": "david@example.com", "timezone": "America/Los_Angeles", "working_hours_start": time(9, 0), "working_hours_end": time(17, 0)},
]

USERS = [
    {"email": "admin@example.com", "password": "admin123", "role": "admin"},
    {"email": "manager@example.com", "password": "manager123", "role": "manager"},
    {"email": "dev@example.com", "password": "dev123", "role": "developer"},
]

TASKS = [
    {"title": "Set up CI/CD pipeline", "description": "Configure GitHub Actions for lint, test, and deploy", "status": TaskStatus.DONE, "priority": TaskPriority.HIGH},
    {"title": "Design login page", "description": "Create Figma mockup for login/register screens", "status": TaskStatus.IN_REVIEW, "priority": TaskPriority.MEDIUM},
    {"title": "Implement task filtering", "description": "Add status and priority filters to task list", "status": TaskStatus.IN_PROGRESS, "priority": TaskPriority.HIGH},
    {"title": "Fix timezone conversion bug", "description": "Due dates show wrong time for non-UTC users", "status": TaskStatus.IN_PROGRESS, "priority": TaskPriority.CRITICAL},
    {"title": "Add developer avatars", "description": "Show profile images on task assignment cards", "status": TaskStatus.TODO, "priority": TaskPriority.LOW},
    {"title": "Write API documentation", "description": "Document all endpoints with request/response examples", "status": TaskStatus.TODO, "priority": TaskPriority.MEDIUM},
    {"title": "Performance audit", "description": "Profile slow queries and optimize N+1 issues", "status": TaskStatus.TODO, "priority": TaskPriority.HIGH},
    {"title": "Mobile responsive layout", "description": "Ensure all pages work on screens >= 320px", "status": TaskStatus.IN_REVIEW, "priority": TaskPriority.MEDIUM},
]


async def seed():
    async with async_session_factory() as session:
        dev_repo = DeveloperRepository(session)
        user_repo = UserRepository(session)
        task_repo = TaskRepository(session)

        existing_devs = await dev_repo.list_all()
        if existing_devs:
            print("Database already seeded, skipping.")
            return

        print("Seeding developers...")
        developers = []
        for data in DEVELOPERS:
            dev = await dev_repo.create(**data)
            developers.append(dev)
            print(f"  Created developer: {dev.name}")

        print("Seeding users...")
        for data in USERS:
            user = await user_repo.create(
                email=data["email"],
                password_hash=hash_password(data["password"]),
                role=data["role"],
            )
            print(f"  Created user: {user.email} ({user.role})")

        print("Seeding tasks...")
        tasks = []
        now = datetime.now(timezone.utc)
        for i, data in enumerate(TASKS):
            due = now + timedelta(days=(i + 1) * 3)
            task = await task_repo.create(
                title=data["title"],
                description=data["description"],
                status=data["status"],
                priority=data["priority"],
                due_date=due,
            )
            tasks.append(task)
            print(f"  Created task: {task.title} [{task.status.value}]")

        print("Assigning developers to tasks...")
        assignments = [
            (tasks[0], developers[3]),
            (tasks[1], developers[0]),
            (tasks[2], developers[0]),
            (tasks[2], developers[1]),
            (tasks[3], developers[2]),
            (tasks[4], developers[3]),
            (tasks[5], developers[1]),
            (tasks[6], developers[0]),
            (tasks[6], developers[2]),
            (tasks[7], developers[1]),
            (tasks[7], developers[3]),
        ]
        for task, dev in assignments:
            assignment = TaskAssignment(task_id=task.id, developer_id=dev.id)
            session.add(assignment)
        await session.flush()

        await session.commit()
        print(f"\nSeeded: {len(developers)} developers, {len(USERS)} users, {len(tasks)} tasks, {len(assignments)} assignments")


if __name__ == "__main__":
    asyncio.run(seed())
