import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.models.user import User
from app.core.security import hash_password

async def create_user(session: AsyncSession, username="test", email="test@mail.com", password="12345"):
    user = User(
        username=username,
        email=email,
        hash_password=hash_password(password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@pytest.mark.asyncio
async def test_register_success(ac: AsyncClient, session: AsyncSession):
    response = await ac.post(
        "/api/v1/users/register",
        params={"username": "alice", "email": "alice@mail.com", "password": "1234"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "alice@mail.com"

    user = await session.get(User, UUID(data["id"]))
    assert user is not None
    assert user.email == "alice@mail.com"


@pytest.mark.asyncio
async def test_register_email_exists(ac: AsyncClient, session: AsyncSession):
    await create_user(session, username="bob", email="bob@mail.com")

    response = await ac.post(
        "/api/v1/users/register",
        params={"username": "bob2", "email": "bob@mail.com", "password": "123"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

@pytest.mark.asyncio
async def test_login_success(ac: AsyncClient, session: AsyncSession):
    await create_user(session, username="testuser", email="login@mail.com", password="pass123")

    response = await ac.post(
        "/api/v1/users/login",
        params={"email": "login@mail.com", "password": "pass123"}
    )

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(ac: AsyncClient, session: AsyncSession):
    await create_user(session, username="kate", email="kate@mail.com", password="1111")

    response = await ac.post(
        "/api/v1/users/login",
        params={"email": "kate@mail.com", "password": "wrong"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
