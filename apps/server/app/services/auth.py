"""Authentication primitives shared by the web UI and future clients."""

import base64
import hashlib
import hmac
import os
import secrets
import time
from datetime import datetime, timedelta

from sqlalchemy import select

from app.core.database import get_session
from app.models.auth import ApiToken, AppSetting, User

SESSION_COOKIE = "mediabridge_session"
SESSION_TTL_SECONDS = 60 * 60 * 24 * 14


def _b64encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode()


def _b64decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def hash_password(password: str, salt: bytes | None = None) -> str:
    salt = salt or secrets.token_bytes(16)
    derived = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    return f"scrypt$16384$8$1${_b64encode(salt)}${_b64encode(derived)}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, n, r, p, salt, expected = encoded.split("$")
        if algorithm != "scrypt":
            return False
        actual = hashlib.scrypt(password.encode(), salt=_b64decode(salt), n=int(n), r=int(r), p=int(p))
        return hmac.compare_digest(actual, _b64decode(expected))
    except (TypeError, ValueError):
        return False


class AuthService:
    async def initialize(self) -> None:
        """Create a persistent signing key and the first administrator."""
        async with get_session() as session:
            secret_setting = await session.get(AppSetting, "auth.session_secret")
            if secret_setting is None:
                session.add(AppSetting(key="auth.session_secret", value=secrets.token_urlsafe(48)))

            result = await session.execute(select(User).limit(1))
            if result.scalar_one_or_none() is None:
                username = os.getenv("MEDIABRIDGE_ADMIN_USERNAME", "admin")
                password = os.getenv("MEDIABRIDGE_ADMIN_PASSWORD")
                if not password:
                    password = secrets.token_urlsafe(18)
                    # The value is intentionally only emitted once, never stored as plaintext.
                    from loguru import logger
                    logger.warning("No MEDIABRIDGE_ADMIN_PASSWORD supplied. Initial admin password: {}", password)
                if len(password) < 12:
                    raise RuntimeError("MEDIABRIDGE_ADMIN_PASSWORD must contain at least 12 characters")
                session.add(User(username=username, password_hash=hash_password(password)))
            await session.commit()

    async def _secret(self) -> str:
        async with get_session() as session:
            setting = await session.get(AppSetting, "auth.session_secret")
            if setting is None:
                raise RuntimeError("Authentication has not been initialized")
            return setting.value

    async def authenticate(self, username: str, password: str) -> User | None:
        async with get_session() as session:
            result = await session.execute(select(User).where(User.username == username))
            user = result.scalar_one_or_none()
            if user is None or not user.is_active or not verify_password(password, user.password_hash):
                return None
            return user

    async def create_session(self, user: User) -> tuple[str, str]:
        csrf_token = secrets.token_urlsafe(24)
        payload = f"{user.id}:{int(time.time()) + SESSION_TTL_SECONDS}:{csrf_token}"
        signature = hmac.new((await self._secret()).encode(), payload.encode(), hashlib.sha256).digest()
        return f"{_b64encode(payload.encode())}.{_b64encode(signature)}", csrf_token

    async def user_from_session(self, value: str | None) -> tuple[User, str] | None:
        if not value or "." not in value:
            return None
        payload_part, signature_part = value.split(".", 1)
        try:
            payload = _b64decode(payload_part).decode()
            expected = hmac.new((await self._secret()).encode(), payload.encode(), hashlib.sha256).digest()
            if not hmac.compare_digest(expected, _b64decode(signature_part)):
                return None
            user_id, expires_at, csrf_token = payload.split(":", 2)
            if int(expires_at) < time.time():
                return None
        except (UnicodeDecodeError, ValueError):
            return None
        async with get_session() as session:
            user = await session.get(User, int(user_id))
            return (user, csrf_token) if user and user.is_active else None

    async def user_from_token(self, value: str | None) -> User | None:
        if not value or not value.startswith("mb_"):
            return None
        token_hash = hashlib.sha256(value.encode()).hexdigest()
        async with get_session() as session:
            result = await session.execute(select(ApiToken).where(ApiToken.token_hash == token_hash))
            token = result.scalar_one_or_none()
            if token is None or token.revoked_at or (token.expires_at and token.expires_at < datetime.now()):
                return None
            user = await session.get(User, token.user_id)
            if user is None or not user.is_active:
                return None
            token.last_used_at = datetime.now()
            await session.commit()
            return user

    async def create_api_token(self, user: User, name: str, expires_in_days: int | None = None) -> tuple[ApiToken, str]:
        raw_token = f"mb_{secrets.token_urlsafe(32)}"
        expires_at = datetime.now() + timedelta(days=expires_in_days) if expires_in_days else None
        token = ApiToken(user_id=user.id, name=name, token_hash=hashlib.sha256(raw_token.encode()).hexdigest(), expires_at=expires_at)
        async with get_session() as session:
            session.add(token)
            await session.commit()
            await session.refresh(token)
        return token, raw_token

    async def list_api_tokens(self, user: User) -> list[ApiToken]:
        async with get_session() as session:
            result = await session.execute(select(ApiToken).where(ApiToken.user_id == user.id).order_by(ApiToken.created_at.desc()))
            return list(result.scalars())

    async def revoke_api_token(self, user: User, token_id: int) -> bool:
        async with get_session() as session:
            token = await session.get(ApiToken, token_id)
            if token is None or token.user_id != user.id:
                return False
            token.revoked_at = datetime.now()
            await session.commit()
            return True
