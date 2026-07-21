import pytest
from httpx import AsyncClient


async def _register_and_login(client: AsyncClient, email: str, password: str = "password123", role: str = "manager") -> str:
    await client.post(
        "/api/auth/register",
        json={"email": email, "password": password, "role": role},
    )
    login_resp = await client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    return login_resp.json()["access_token"]


class TestTasksAPI:
    async def test_create_task_returns_201(self, client: AsyncClient):
        token = await _register_and_login(client, "creator@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.post(
            "/api/tasks",
            json={"title": "New Task", "priority": "high"},
            headers=headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Task"
        assert data["priority"] == "high"

    async def test_create_task_without_auth_returns_401(self, client: AsyncClient):
        response = await client.post(
            "/api/tasks",
            json={"title": "Unauthorized Task"},
        )
        assert response.status_code == 401

    async def test_list_tasks_returns_200(self, client: AsyncClient):
        token = await _register_and_login(client, "lister@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.get("/api/tasks", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "tasks" in data
        assert "total" in data

    async def test_get_task_by_id_returns_200(self, client: AsyncClient):
        token = await _register_and_login(client, "getter@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        create_resp = await client.post(
            "/api/tasks",
            json={"title": "Get Me Task"},
            headers=headers,
        )
        task_id = create_resp.json()["id"]

        response = await client.get(f"/api/tasks/{task_id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Get Me Task"

    async def test_update_task_returns_200(self, client: AsyncClient):
        token = await _register_and_login(client, "updater@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        create_resp = await client.post(
            "/api/tasks",
            json={"title": "Original Title"},
            headers=headers,
        )
        task_id = create_resp.json()["id"]

        response = await client.put(
            f"/api/tasks/{task_id}",
            json={"title": "Updated Title"},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"

    async def test_assign_developer_returns_200(self, client: AsyncClient):
        token = await _register_and_login(client, "assigner@example.com", role="admin")
        headers = {"Authorization": f"Bearer {token}"}

        create_resp = await client.post(
            "/api/tasks",
            json={"title": "Assign Task"},
            headers=headers,
        )
        task_id = create_resp.json()["id"]

        dev_resp = await client.post(
            "/api/developers",
            json={"name": "Dev", "email": "dev_assign@example.com"},
            headers=headers,
        )
        developer_id = dev_resp.json()["id"]

        response = await client.post(
            f"/api/tasks/{task_id}/assign",
            json={"developer_ids": [developer_id]},
            headers=headers,
        )
        assert response.status_code == 200

    async def test_unassign_developer_returns_200(self, client: AsyncClient):
        token = await _register_and_login(client, "unassigner@example.com", role="admin")
        headers = {"Authorization": f"Bearer {token}"}

        create_resp = await client.post(
            "/api/tasks",
            json={"title": "Unassign Task"},
            headers=headers,
        )
        task_id = create_resp.json()["id"]

        dev_resp = await client.post(
            "/api/developers",
            json={"name": "Dev", "email": "dev_unassign@example.com"},
            headers=headers,
        )
        developer_id = dev_resp.json()["id"]

        await client.post(
            f"/api/tasks/{task_id}/assign",
            json={"developer_ids": [developer_id]},
            headers=headers,
        )

        response = await client.delete(
            f"/api/tasks/{task_id}/assignments/{developer_id}",
            headers=headers,
        )
        assert response.status_code == 200
