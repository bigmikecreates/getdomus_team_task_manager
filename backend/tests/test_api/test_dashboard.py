import pytest
from datetime import datetime, timedelta, timezone
from httpx import AsyncClient


async def _register_and_login(
    client: AsyncClient, email: str, password: str = "password123", role: str = "admin"
) -> str:
    await client.post(
        "/api/auth/register",
        json={"email": email, "password": password, "role": role},
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
        assert "by_assignee" in data

    async def test_dashboard_stats_with_tasks(self, client: AsyncClient):
        token = await _register_and_login(client, "statstask@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        for _ in range(2):
            resp = await client.post(
                "/api/tasks",
                json={"title": "Todo Task", "status": "todo", "priority": "high"},
                headers=headers,
            )
            assert resp.status_code == 201
        resp = await client.post(
            "/api/tasks",
            json={"title": "Done Task", "status": "done", "priority": "low"},
            headers=headers,
        )
        assert resp.status_code == 201

        response = await client.get("/api/dashboard/stats", headers=headers)
        data = response.json()

        assert data["total_tasks"] == 3
        by_status = {s["status"]: s["count"] for s in data["by_status"]}
        assert by_status["todo"] == 2
        assert by_status["done"] == 1

    async def test_dashboard_overview_returns_200(self, client: AsyncClient):
        token = await _register_and_login(client, "overview@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.get("/api/dashboard/overview", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "stats" in data
        assert "overdue_tasks" in data
        assert "critical_tasks" in data
        assert "upcoming_tasks" in data
        assert "recent_tasks" in data

    async def test_dashboard_overview_critical_count(self, client: AsyncClient):
        token = await _register_and_login(client, "critical@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        await client.post(
            "/api/tasks",
            json={"title": "Critical Task", "priority": "critical"},
            headers=headers,
        )
        await client.post(
            "/api/tasks",
            json={"title": "Normal Task", "priority": "high"},
            headers=headers,
        )

        response = await client.get("/api/dashboard/overview", headers=headers)
        data = response.json()

        assert data["critical_tasks"] == 1

    async def test_dashboard_overview_upcoming_tasks(self, client: AsyncClient):
        token = await _register_and_login(client, "upcoming@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        now = datetime.now(timezone.utc)
        await client.post(
            "/api/tasks",
            json={
                "title": "Soon Task",
                "due_date": (now + timedelta(days=1)).isoformat(),
            },
            headers=headers,
        )
        await client.post(
            "/api/tasks",
            json={
                "title": "Later Task",
                "due_date": (now + timedelta(days=7)).isoformat(),
            },
            headers=headers,
        )

        response = await client.get("/api/dashboard/overview", headers=headers)
        data = response.json()

        assert len(data["upcoming_tasks"]) == 2

    async def test_dashboard_overview_overdue_count(self, client: AsyncClient):
        token = await _register_and_login(client, "overdue2@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        await client.post(
            "/api/tasks",
            json={
                "title": "Overdue Task",
                "due_date": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
            },
            headers=headers,
        )
        await client.post(
            "/api/tasks",
            json={
                "title": "On Time Task",
                "due_date": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
            },
            headers=headers,
        )

        response = await client.get("/api/dashboard/overview", headers=headers)
        data = response.json()

        assert data["overdue_tasks"] == 1
