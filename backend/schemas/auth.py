from pydantic import BaseModel, EmailStr

from backend.models.user import UserRole


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.DEVELOPER


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    email: str
    role: UserRole
    developer_id: str | None = None

    model_config = {"from_attributes": True}
