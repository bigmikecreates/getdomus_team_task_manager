import pytest
from httpx import AsyncClient


class TestAuthAPI:
    async def test_register_returns_201(self, client: AsyncClient):
        response = await client.post(
            "/api/auth/register",
            json={"email": "new@example.com", "password": "securepassword123"},
        )
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["email"] == "new@example.com"

    async def test_register_duplicate_email_returns_400(self, client: AsyncClient):
        await client.post(
            "/api/auth/register",
            json={"email": "dup@example.com", "password": "password1"},
        )
        response = await client.post(
            "/api/auth/register",
            json={"email": "dup@example.com", "password": "password2"},
        )
        assert response.status_code == 400

    async def test_login_returns_200_with_token(self, client: AsyncClient):
        await client.post(
            "/api/auth/register",
            json={"email": "login@example.com", "password": "mypassword"},
        )
        response = await client.post(
            "/api/auth/login",
            json={"email": "login@example.com", "password": "mypassword"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    async def test_login_wrong_password_returns_401(self, client: AsyncClient):
        await client.post(
            "/api/auth/register",
            json={"email": "wrong@example.com", "password": "correctpassword"},
        )
        response = await client.post(
            "/api/auth/login",
            json={"email": "wrong@example.com", "password": "wrongpassword"},
        )
        assert response.status_code == 401

    async def test_me_returns_current_user(self, client: AsyncClient):
        await client.post(
            "/api/auth/register",
            json={"email": "me@example.com", "password": "mypassword"},
        )
        login_resp = await client.post(
            "/api/auth/login",
            json={"email": "me@example.com", "password": "mypassword"},
        )
        token = login_resp.json()["access_token"]

        response = await client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "me@example.com"

    async def test_me_without_token_returns_401(self, client: AsyncClient):
        response = await client.get("/api/auth/me")
        assert response.status_code == 401
