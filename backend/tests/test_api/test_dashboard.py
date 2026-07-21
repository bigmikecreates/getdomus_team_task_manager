import pytest
from httpx import AsyncClient


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


class TestDashboardAPI:
    async def test_dashboard_stats_returns_200(self, client: AsyncClient):
        token = await _register_and_login(client, "dashboard@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.get("/api/dashboard/stats", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "total_tasks" in data
        assert "by_status" in data
        assert "by_priority" in data

    async def test_dashboard_overview_returns_200(self, client: AsyncClient):
        token = await _register_and_login(client, "overview@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.get("/api/dashboard/overview", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "stats" in data
        assert "recent_tasks" in data
        assert "overdue_tasks" in data
