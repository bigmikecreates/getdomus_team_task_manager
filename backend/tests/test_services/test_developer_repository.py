import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.developer import Developer
from backend.repositories.developer_repository import DeveloperRepository


class TestDeveloperRepository:
    async def test_create_developer(self, db_session: AsyncSession):
        repo = DeveloperRepository(db_session)
        dev = await repo.create(
            name="Test Dev",
            email="testdev@example.com",
            timezone="Europe/London",
        )

        assert dev.id is not None
        assert dev.name == "Test Dev"
        assert dev.email == "testdev@example.com"
        assert dev.timezone == "Europe/London"

    async def test_get_developer_by_id(self, db_session: AsyncSession):
        repo = DeveloperRepository(db_session)
        dev = await repo.create(name="Find Me", email="findme@example.com")
        found = await repo.get(dev.id)

        assert found is not None
        assert found.id == dev.id

    async def test_get_developer_by_email(self, db_session: AsyncSession):
        repo = DeveloperRepository(db_session)
        dev = await repo.create(name="Email Dev", email="emaildev@example.com")
        found = await repo.get_by_email("emaildev@example.com")

        assert found is not None
        assert found.id == dev.id

    async def test_get_nonexistent_email_returns_none(self, db_session: AsyncSession):
        repo = DeveloperRepository(db_session)
        found = await repo.get_by_email("nonexistent@example.com")

        assert found is None

    async def test_list_all_developers(self, db_session: AsyncSession):
        repo = DeveloperRepository(db_session)
        await repo.create(name="Dev 1", email="dev1@example.com")
        await repo.create(name="Dev 2", email="dev2@example.com")

        devs = await repo.list_all()

        assert len(devs) == 2

    async def test_update_developer(self, db_session: AsyncSession):
        repo = DeveloperRepository(db_session)
        dev = await repo.create(name="Old Name", email="update@example.com")

        updated = await repo.update(dev.id, name="New Name")

        assert updated is not None
        assert updated.name == "New Name"

    async def test_delete_developer(self, db_session: AsyncSession):
        repo = DeveloperRepository(db_session)
        dev = await repo.create(name="Delete Me", email="deleteme@example.com")

        result = await repo.delete(dev.id)

        assert result is True
        found = await repo.get(dev.id)
        assert found is None

    async def test_delete_nonexistent_developer_returns_false(self, db_session: AsyncSession):
        repo = DeveloperRepository(db_session)
        result = await repo.delete("nonexistent-id")

        assert result is False
