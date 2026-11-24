from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


# TENANT
class TenantResponse(BaseModel):
    id: int
    name: str
    slug: str
    subdomain: str
    is_active: bool
    primary_color: str
    secondary_color: str
    logo_url: str | None
    tagline: str | None

    model_config = ConfigDict(from_attributes=True)


# USER
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    tenant_id: int | None
    name: str
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ARTICLE
class ArticleCreate(BaseModel):
    title: str
    content: str
    status: str = "draft"


class ArticleResponse(BaseModel):
    id: int
    tenant_id: int
    author_id: int | None
    title: str
    content: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# BOOK
class BookCreate(BaseModel):
    title: str
    description: str | None = None
    published_year: int | None = None
    status: str = "draft"


class BookResponse(BaseModel):
    id: int
    tenant_id: int
    author_id: int | None
    title: str
    description: str | None
    published_year: int | None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TenantAdminCreate(BaseModel):
    tenant_id: int
    name: str
    email: EmailStr
    password: str