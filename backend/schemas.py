# backend/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ── User schemas ──────────────────────────────────────
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    class Config:
        from_attributes = True


# ── Quote schemas ─────────────────────────────────────
class QuoteCreate(BaseModel):
    text: str
    author: str
    category: Optional[str] = None
    source: Optional[str] = None


class QuoteUpdate(BaseModel):
    text: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    source: Optional[str] = None


class QuoteOut(BaseModel):
    id: int
    text: str
    author: str
    category: Optional[str]
    source: Optional[str]
    date_added: datetime
    user_id: int
    class Config:
        from_attributes = True


# ── Token schemas (for login) ──────────────────────────
class Token(BaseModel):
    access_token: str
    token_type: str
