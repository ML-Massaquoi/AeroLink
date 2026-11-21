from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class RoleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None
    permissions: list[str] = []


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: str
    is_active: bool
    role: RoleOut
    last_login_at: datetime | None = None
    created_at: datetime


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=128)
    password: str = Field(min_length=10, max_length=128)
    role_id: int


class UserList(BaseModel):
    items: list[UserOut]
    total: int


class Message(BaseModel):
    detail: str


class PermissionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codename: str
    description: str | None = None


class AuditEventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int | None = None
    action: str
    entity_type: str
    entity_id: str | None = None
    reason: str | None = None
    created_at: datetime


class AuditEventList(BaseModel):
    items: list[AuditEventOut]
    total: int


class HealthStatus(BaseModel):
    status: str
    app: str
    database: str
