import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.models.user import User
from app.core.security import hash_password

async def create_user(
        session: AsyncSession,
        username="username",
        email="user@example.com",
        password="string12345"
):
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
async def test_register_success(
        ac: AsyncClient,
        session: AsyncSession
):
    response = await ac.post(
        "/api/v1/users/register",
        json = {
            "email": "alice@mail.com",
            "username": "username",
            "password": "string12345"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "alice@mail.com"

    user = await session.get(User, UUID(data["id"]))
    assert user is not None
    assert user.email == "alice@mail.com"

@pytest.mark.asyncio
async def test_register_email_exists(
        ac: AsyncClient,
        session: AsyncSession
):
    await create_user(session, username="bob123best", email="bob@mail.com")

    response = await ac.post(
        "/api/v1/users/register",
        json={"username": "bob2new", "email": "bob@mail.com", "password": "strongpass123"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Пользователь с такой почтой уже существует"

@pytest.mark.asyncio
async def test_login_success(
        ac: AsyncClient,
        session: AsyncSession
):
    await create_user(session, username="testuser", email="login@mail.com", password="strongpass123")

    response = await ac.post(
        "/api/v1/users/login",
        json={"email": "login@mail.com", "password": "strongpass123"}
    )

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_wrong_password(
        ac: AsyncClient,
        session: AsyncSession
):
    await create_user(session, username="kate_new_ac", email="kate@mail.com", password="qwerty1234A")

    response = await ac.post(
        "/api/v1/users/login",
        json={"email": "kate@mail.com", "password": "qw3sdfDwy1w23dA"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Неверный логин или пароль"

@pytest.mark.asyncio
async def test_register_invalid_username(ac: AsyncClient):
    response = await ac.post(
        "/api/v1/users/register",
        json={"username": "abc", "email": "valid@mail.com", "password": "StrongPass123"}
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"].startswith("String should have at least")

@pytest.mark.asyncio
async def test_register_invalid_email(ac: AsyncClient):
    response = await ac.post(
        "/api/v1/users/register",
        json={"username": "validName", "email": "not-email", "password": "StrongPass123"}
    )

    assert response.status_code == 422
    assert "value is not a valid email address" in response.json()["detail"][0]["msg"]

@pytest.mark.asyncio
async def test_register_password_too_short(ac: AsyncClient):
    response = await ac.post(
        "/api/v1/users/register",
        json={"username": "validName", "email": "user@mail.com", "password": "short"}
    )

    assert response.status_code == 422
    assert "Пароль должен быть больше 10 символов" in response.json()["detail"][0]["msg"]

@pytest.mark.asyncio
async def test_register_password_no_digit(ac: AsyncClient):
    response = await ac.post(
        "/api/v1/users/register",
        json={"username": "validName", "email": "user@mail.com", "password": "NoDigitsHereAA"}
    )

    assert response.status_code == 422
    assert "Пароль должен содержать цифру" in response.json()["detail"][0]["msg"]

@pytest.mark.asyncio
async def test_register_password_no_letter(ac: AsyncClient):
    response = await ac.post(
        "/api/v1/users/register",
        json={"username": "validName", "email": "user@mail.com", "password": "123456789012345"}
    )

    assert response.status_code == 422
    assert "Пароль должен содержать букву" in response.json()["detail"][0]["msg"]
