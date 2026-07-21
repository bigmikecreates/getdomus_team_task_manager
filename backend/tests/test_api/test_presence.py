"""Tests for the presence heartbeat API endpoint."""

import pytest
from httpx import AsyncClient

from backend.core.security import create_access_token
from backend.models.user import User, UserRole
from backend.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession


async def _register_and_login(client: AsyncClient, email: str, password: str = "password123") -> str:
    await client.post(
        "/api/auth/register",
        json={"email": email, "password": password},
    )
    login_resp = await client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    return login_resp.json()["access_token"]


class TestPresenceAPI:
    async def test_heartbeat_returns_200(self, client: AsyncClient):
        token = await _register_and_login(client, "hb@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.post("/api/presence/heartbeat", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    async def test_heartbeat_requires_auth(self, client: AsyncClient):
        response = await client.post("/api/presence/heartbeat")
        assert response.status_code in (401, 403)
