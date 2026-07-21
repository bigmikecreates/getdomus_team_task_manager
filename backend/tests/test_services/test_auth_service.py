import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.user import User, UserRole
from backend.services.auth_service import AuthService
from backend.core.security import verify_password


class TestAuthService:
    async def test_register_user(self, db_session: AsyncSession):
        service = AuthService(db_session)
        user = await service.register(
            email="new@example.com",
            password="securepassword123",
            role=UserRole.DEVELOPER,
        )

        assert user.id is not None
        assert user.email == "new@example.com"
        assert user.role == UserRole.DEVELOPER
        assert verify_password("securepassword123", user.password_hash)

    async def test_register_duplicate_email_raises(self, db_session: AsyncSession):
        service = AuthService(db_session)
        await service.register(email="dup@example.com", password="password1")

        with pytest.raises(ValueError, match="already registered"):
            await service.register(email="dup@example.com", password="password2")

    async def test_login_success(self, db_session: AsyncSession):
        service = AuthService(db_session)
        await service.register(email="login@example.com", password="mypassword")

        token = await service.login(email="login@example.com", password="mypassword")

        assert token is not None
        assert len(token) > 0

    async def test_login_wrong_password_raises(self, db_session: AsyncSession):
        service = AuthService(db_session)
        await service.register(email="wrong@example.com", password="correctpassword")

        with pytest.raises(ValueError, match="Invalid credentials"):
            await service.login(email="wrong@example.com", password="wrongpassword")

    async def test_login_nonexistent_user_raises(self, db_session: AsyncSession):
        service = AuthService(db_session)

        with pytest.raises(ValueError, match="Invalid credentials"):
            await service.login(email="nonexistent@example.com", password="password")
