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


class TestDevelopersAPI:
    async def test_list_developers_returns_200(self, client: AsyncClient):
        token = await _register_and_login(client, "viewer@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.get("/api/developers", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    async def test_create_developer_requires_admin(self, client: AsyncClient):
        token = await _register_and_login(client, "nonadmin@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.post(
            "/api/developers",
            json={"name": "New Dev", "email": "newdev@example.com"},
            headers=headers,
        )
        assert response.status_code == 403

    async def test_create_developer_as_admin_returns_201(self, client: AsyncClient):
        await client.post(
            "/api/auth/register",
            json={"email": "admin@example.com", "password": "password123", "role": "admin"},
        )
        login_resp = await client.post(
            "/api/auth/login",
            json={"email": "admin@example.com", "password": "password123"},
        )
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.post(
            "/api/developers",
            json={"name": "Admin Dev", "email": "admindev@example.com"},
            headers=headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Admin Dev"

    async def test_update_developer_returns_200(self, client: AsyncClient):
        await client.post(
            "/api/auth/register",
            json={"email": "admin2@example.com", "password": "password123", "role": "admin"},
        )
        login_resp = await client.post(
            "/api/auth/login",
            json={"email": "admin2@example.com", "password": "password123"},
        )
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        dev_resp = await client.post(
            "/api/developers",
            json={"name": "Old Name", "email": "oldname@example.com"},
            headers=headers,
        )
        dev_id = dev_resp.json()["id"]

        response = await client.put(
            f"/api/developers/{dev_id}",
            json={"name": "New Name"},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New Name"
