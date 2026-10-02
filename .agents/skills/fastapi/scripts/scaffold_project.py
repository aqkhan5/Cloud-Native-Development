#!/usr/bin/env python3
"""
FastAPI Production Project Scaffolder

This script initializes a professional production-ready FastAPI project structure
with SQLAlchemy, Pydantic settings, JWT authentication, and pytest configurations.
"""

import os
import argparse
from pathlib import Path

def create_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"  Created: {path}")

def scaffold(target_dir: Path):
    print(f"🚀 Scaffolding FastAPI project in: {target_dir}")
    
    # 1. Main files
    create_file(target_dir / "app" / "__init__.py", "")
    
    create_file(target_dir / "app" / "main.py", """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import auth, users

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])
app.include_router(users.router, prefix=settings.API_V1_STR, tags=["users"])

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}
""")

    create_file(target_dir / "app" / "config.py", """
from typing import List, Union
from pydantic import AnyHttpUrl, BeforeValidator, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Annotated

def parse_cors(v: Union[str, List[str]]) -> List[str]:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, (list, str)):
        return v
    raise ValueError(v)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Production API"
    
    # SECRET_KEY should be changed in production!
    SECRET_KEY: str = "60c8cb0802c638148b3b7e77a16f80721bc620021c168fefcda09b83c799a777"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./sql_app.db"
    
    BACKEND_CORS_ORIGINS: Annotated[
        List[AnyHttpUrl], BeforeValidator(parse_cors)
    ] = []

settings = Settings()
""")

    create_file(target_dir / "app" / "database.py", """
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# Create engine
connect_args = {"check_same_thread": False} if settings.SQLALCHEMY_DATABASE_URI.startswith("sqlite") else {}
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, connect_args=connect_args)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base
Base = declarative_base()
""")

    create_file(target_dir / "app" / "dependencies.py", """
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.config import settings
from app.database import SessionLocal
from app.models.user import User

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data_sub = payload.get("sub")
        if token_data_sub is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = db.query(User).filter(User.email == token_data_sub).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
""")

    # 2. Models
    create_file(target_dir / "app" / "models" / "__init__.py", "")
    
    create_file(target_dir / "app" / "models" / "user.py", """
from sqlalchemy import Boolean, Column, Integer, String
from pydantic import BaseModel, EmailStr
from app.database import Base

# SQLAlchemy Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)

# Pydantic Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None
    is_active: bool | None = True

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
""")

    # 3. Routers
    create_file(target_dir / "app" / "routers" / "__init__.py", "")
    
    create_file(target_dir / "app" / "routers" / "auth.py", """
from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.config import settings
from app.dependencies import get_db
from app.models.user import Token, User
from app.crud.user import authenticate_user, create_access_token

router = APIRouter(prefix="/auth")

@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=create_access_token(
            user.email, expires_delta=access_token_expires
        ),
        token_type="bearer",
    )
""")

    create_file(target_dir / "app" / "routers" / "users.py", """
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models.user import User, UserCreate, UserResponse
from app.crud.user import get_user_by_email, create_user

router = APIRouter(prefix="/users")

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)) -> Any:
    user = get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists."
        )
    return create_user(db, user_in=user_in)

@router.get("/me", response_model=UserResponse)
def read_user_me(current_user: User = Depends(get_current_user)) -> Any:
    return current_user
""")

    # 4. CRUD
    create_file(target_dir / "app" / "crud" / "__init__.py", "")
    
    create_file(target_dir / "app" / "crud" / "user.py", """
from datetime import datetime, timedelta, timezone
from typing import Any
import jwt
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from app.config import settings
from app.models.user import User, UserCreate

password_hash = PasswordHash.recommended()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_user(db: Session, user_in: UserCreate) -> User:
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        full_name=user_in.full_name,
        is_active=user_in.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_access_token(subject: str | Any, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
""")

    # 5. Tests
    create_file(target_dir / "tests" / "__init__.py", "")
    
    create_file(target_dir / "tests" / "conftest.py", """
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database import Base
from app.main import app
from app.dependencies import get_db

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db() -> Generator:
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db) -> Generator:
    def override_get_db():
        try:
            yield db
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
""")

    create_file(target_dir / "tests" / "test_auth.py", """
def test_register_and_login(client):
    # Register user
    response = client.post(
        "/api/v1/users/",
        json={"email": "test@example.com", "password": "securepassword", "full_name": "Test User"},
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
    
    # Login user
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "securepassword"},
    )
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    
    # Get current user details
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
""")

    # 6. Config files
    create_file(target_dir / ".env.example", """
PROJECT_NAME="FastAPI Production API"
SECRET_KEY="replace-this-with-a-random-hex-string-for-production"
SQLALCHEMY_DATABASE_URI="sqlite:///./sql_app.db"
BACKEND_CORS_ORIGINS="http://localhost:3000,http://localhost:8000"
""")

    create_file(target_dir / ".env", """
PROJECT_NAME="FastAPI Production API (Dev)"
SECRET_KEY="60c8cb0802c638148b3b7e77a16f80721bc620021c168fefcda09b83c799a777"
SQLALCHEMY_DATABASE_URI="sqlite:///./sql_app.db"
BACKEND_CORS_ORIGINS="http://localhost:3000,http://localhost:8000"
""")

    create_file(target_dir / "pyproject.toml", """
[project]
name = "fastapi-production-api"
version = "0.1.0"
description = "A professional production-ready FastAPI project structure"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.110.0",
    "uvicorn[standard]>=0.28.0",
    "sqlalchemy>=2.0.0",
    "pydantic[email]>=2.6.0",
    "pydantic-settings>=2.2.0",
    "pyjwt>=2.8.0",
    "pwdlib[argon2]>=0.2.0",
]

[dependency-groups]
dev = [
    "pytest>=8.0.0",
    "httpx>=0.27.0",
]
""")

    create_file(target_dir / "README.md", """
# FastAPI Production API

A structured, professional FastAPI production repository layout.

## Getting Started

1. Set up a virtual environment and install dependencies:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -e .
   uv pip install -e ".[dev]"
   ```

2. Run development server:
   ```bash
   fastapi dev app/main.py
   ```

3. Run tests:
   ```bash
   pytest
   ```
""")

    print("\n✅ Scaffolding complete! Check output directory.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold a production FastAPI project.")
    parser.add_argument("target_dir", type=str, nargs="?", default=".", help="Target directory for scaffolding.")
    args = parser.parse_args()
    
    scaffold(Path(args.target_dir).resolve())
