import pytest

from app.core.database import get_session, init_db
from app.services.auth import AuthService, hash_password, verify_password


def test_password_hash_is_salted_and_verifiable():
    encoded = hash_password("correct horse battery staple")
    assert encoded.startswith("scrypt$")
    assert verify_password("correct horse battery staple", encoded)
    assert not verify_password("wrong password", encoded)


@pytest.mark.asyncio
async def test_session_and_api_token_lifecycle(tmp_path, monkeypatch):
    database_url = f"sqlite+aiosqlite:///{tmp_path / 'auth.db'}"
    await init_db(database_url)
    monkeypatch.setenv("MEDIABRIDGE_ADMIN_USERNAME", "owner")
    monkeypatch.setenv("MEDIABRIDGE_ADMIN_PASSWORD", "a-long-test-password")
    service = AuthService()
    await service.initialize()

    user = await service.authenticate("owner", "a-long-test-password")
    assert user is not None
    session, csrf_token = await service.create_session(user)
    session_user = await service.user_from_session(session)
    assert session_user is not None
    assert session_user[0].username == "owner"
    assert session_user[1] == csrf_token

    token, raw_token = await service.create_api_token(user, "browser-extension", 30)
    assert raw_token.startswith("mb_")
    assert (await service.user_from_token(raw_token)).username == "owner"
    assert await service.revoke_api_token(user, token.id)
    assert await service.user_from_token(raw_token) is None
