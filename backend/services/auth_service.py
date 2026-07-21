from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.security import create_access_token, hash_password, verify_password
from backend.models.user import User, UserRole
from backend.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = UserRepository(session)

    async def register(self, email: str, password: str, role: UserRole = UserRole.DEVELOPER) -> User:
        existing = await self.repo.get_by_email(email)
        if existing is not None:
            raise ValueError("Email already registered")

        user = await self.repo.create(
            email=email,
            password_hash=hash_password(password),
            role=role,
        )
        return user

    async def login(self, email: str, password: str) -> str:
        user = await self.repo.get_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")

        return create_access_token(data={"sub": user.id, "role": user.role})
