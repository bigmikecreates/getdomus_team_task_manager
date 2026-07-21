from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.developer import Developer


class DeveloperRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, name: str, email: str, timezone: str = "UTC", **kwargs) -> Developer:
        developer = Developer(name=name, email=email, timezone=timezone, **kwargs)
        self.session.add(developer)
        await self.session.flush()
        return developer

    async def get(self, developer_id: str) -> Developer | None:
        result = await self.session.execute(select(Developer).where(Developer.id == developer_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Developer | None:
        result = await self.session.execute(select(Developer).where(Developer.email == email))
        return result.scalar_one_or_none()

    async def list_all(self) -> list[Developer]:
        result = await self.session.execute(select(Developer))
        return list(result.scalars().all())

    async def update(self, developer_id: str, **kwargs) -> Developer | None:
        developer = await self.get(developer_id)
        if developer is None:
            return None
        for key, value in kwargs.items():
            if value is not None:
                setattr(developer, key, value)
        await self.session.flush()
        return developer
