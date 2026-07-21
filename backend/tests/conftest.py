from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.core.database import Base, get_db
from backend.core.security import create_access_token, hash_password
from backend.main import app
from backend.models.developer import Developer
from backend.models.task import Task, TaskStatus, TaskPriority
from backend.models.user import User, UserRole


TEST_DATABASE_URL = "sqlite+aiosqlite:///file::memory:?cache=shared&uri=true"


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    connection = await test_engine.connect()
    transaction = await connection.begin()
    session_factory = async_sessionmaker(bind=connection, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        yield session
    await transaction.rollback()
    await connection.close()


@pytest.fixture
async def client(test_engine) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        async with AsyncSession(bind=test_engine, expire_on_commit=False) as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
    async with test_engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())


@pytest.fixture
async def sample_developer(db_session: AsyncSession) -> Developer:
    developer = Developer(
        name="John Doe",
        email="john@example.com",
        timezone="America/New_York",
    )
    db_session.add(developer)
    await db_session.flush()
    return developer


@pytest.fixture
async def sample_user(db_session: AsyncSession) -> User:
    user = User(
        email="user@example.com",
        password_hash=hash_password("testpassword123"),
        role=UserRole.DEVELOPER,
    )
    db_session.add(user)
    await db_session.flush()
    return user


@pytest.fixture
async def sample_admin_user(db_session: AsyncSession) -> User:
    user = User(
        email="admin@example.com",
        password_hash=hash_password("adminpassword123"),
        role=UserRole.ADMIN,
    )
    db_session.add(user)
    await db_session.flush()
    return user


@pytest.fixture
async def sample_manager_user(db_session: AsyncSession) -> User:
    user = User(
        email="manager@example.com",
        password_hash=hash_password("managerpassword123"),
        role=UserRole.MANAGER,
    )
    db_session.add(user)
    await db_session.flush()
    return user


@pytest.fixture
async def sample_task(db_session: AsyncSession) -> Task:
    task = Task(
        title="Test Task",
        description="A test task description",
        status=TaskStatus.TODO,
        priority=TaskPriority.MEDIUM,
    )
    db_session.add(task)
    await db_session.flush()
    return task


def create_auth_headers(user: User) -> dict[str, str]:
    token = create_access_token(data={"sub": user.id, "role": user.role})
    return {"Authorization": f"Bearer {token}"}
