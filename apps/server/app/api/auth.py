"""Web-session and personal access-token endpoints."""

import os

from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel, Field

from app.services.auth import AuthService, SESSION_COOKIE, SESSION_TTL_SECONDS

router = APIRouter()


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=256)


class CreateTokenRequest(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    expires_in_days: int | None = Field(default=None, ge=1, le=3650)


def _auth_service(request: Request) -> AuthService:
    return request.app.state.container.auth_service


def _current_user(request: Request):
    user = getattr(request.state, "auth_user", None)
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user


def _secure_cookie() -> bool:
    return os.getenv("MEDIABRIDGE_COOKIE_SECURE", "true").lower() not in {"0", "false", "no"}


def _serialize_user(user, csrf_token: str | None = None) -> dict:
    data = {"id": user.id, "username": user.username, "role": user.role}
    if csrf_token:
        data["csrf_token"] = csrf_token
    return data


@router.post("/login")
async def login(request: Request, response: Response, body: LoginRequest):
    service = _auth_service(request)
    user = await service.authenticate(body.username, body.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    session, csrf_token = await service.create_session(user)
    response.set_cookie(
        key=SESSION_COOKIE,
        value=session,
        max_age=SESSION_TTL_SECONDS,
        httponly=True,
        secure=_secure_cookie(),
        samesite="strict",
        path="/",
    )
    return {"code": 0, "message": "Login successful", "data": _serialize_user(user, csrf_token)}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(SESSION_COOKIE, path="/", httponly=True, secure=_secure_cookie(), samesite="strict")
    return {"code": 0, "message": "Logged out", "data": None}


@router.get("/me")
async def me(request: Request):
    user = _current_user(request)
    return {"code": 0, "message": "Authenticated", "data": _serialize_user(user, getattr(request.state, "csrf_token", None))}


@router.post("/tokens")
async def create_token(request: Request, body: CreateTokenRequest):
    user = _current_user(request)
    token, raw_token = await _auth_service(request).create_api_token(user, body.name, body.expires_in_days)
    return {"code": 0, "message": "Token created. Store it now; it cannot be shown again.", "data": {"id": token.id, "name": token.name, "token": raw_token, "expires_at": token.expires_at}}


@router.get("/tokens")
async def list_tokens(request: Request):
    user = _current_user(request)
    tokens = await _auth_service(request).list_api_tokens(user)
    return {"code": 0, "message": "Token list retrieved", "data": [{"id": token.id, "name": token.name, "created_at": token.created_at, "last_used_at": token.last_used_at, "expires_at": token.expires_at, "revoked_at": token.revoked_at} for token in tokens]}


@router.delete("/tokens/{token_id}")
async def revoke_token(request: Request, token_id: int):
    if not await _auth_service(request).revoke_api_token(_current_user(request), token_id):
        raise HTTPException(status_code=404, detail="Token not found")
    return {"code": 0, "message": "Token revoked", "data": None}
