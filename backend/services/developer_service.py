from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.developer import Developer
from backend.repositories.developer_repository import DeveloperRepository


class DeveloperService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = DeveloperRepository(session)

    async def create_developer(self, name: str, email: str, timezone: str = "UTC", **kwargs) -> Developer:
        return await self.repo.create(name=name, email=email, timezone=timezone, **kwargs)

    async def get_developer(self, developer_id: str) -> Developer | None:
        return await self.repo.get(developer_id)

    async def list_developers(self) -> list[Developer]:
        return await self.repo.list_all()

    async def update_developer(self, developer_id: str, **kwargs) -> Developer | None:
        return await self.repo.update(developer_id, **kwargs)
