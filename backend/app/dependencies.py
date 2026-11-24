from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Tenant, User
from app.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_tenant(
    request: Request,
    db: Session = Depends(get_db),
):
    host = request.headers.get("host", "").split(":")[0].lower()

    # Local development: use X-Tenant-Slug when accessing localhost.
    if host in ("localhost", "127.0.0.1"):
        slug = request.headers.get("X-Tenant-Slug")
    else:
        slug = host.split(".")[0]

    if not slug:
        raise HTTPException(status_code=400, detail="Tenant not specified")

    tenant = db.query(Tenant).filter(
        Tenant.subdomain == slug,
        Tenant.is_active == True
    ).first()

    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    return tenant


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(User).filter(
        User.id == user_id,
        User.is_active == True
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found or inactive")

    return user


def require_tenant_access(
    tenant: Tenant = Depends(get_current_tenant),
    user: User = Depends(get_current_user),
):
    if user.role == "super_admin":
        return tenant

    if user.tenant_id != tenant.id:
        raise HTTPException(status_code=403, detail="Access denied for this tenant")

    return tenant