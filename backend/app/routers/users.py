from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models import User
from app.schemas import UserLogin, UserResponse, TokenResponse
from app.security import verify_password, create_access_token

from app.dependencies import require_tenant_access
from app.models import Tenant
from app.schemas import TenantAdminCreate
from app.security import hash_password

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.email == data.email,
        User.is_active == True
    ).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(user.id, user.tenant_id, user.role)

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_me(user: User = Depends(get_current_user)):
    return user


@router.post("/tenant-admin")
def create_tenant_admin(
    data: TenantAdminCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user.role != "super_admin":
        raise HTTPException(status_code=403, detail="Super Admin access required")

    tenant = db.query(Tenant).filter(
        Tenant.id == data.tenant_id,
        Tenant.is_active == True
    ).first()

    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    existing = db.query(User).filter(User.email == data.email).first()

    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    new_user = User(
        tenant_id=tenant.id,
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
        role="tenant_admin",
        is_active=True,
    )

    db.add(new_user)
    db.commit()

    return {"message": "Tenant admin created successfully"}