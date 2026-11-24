from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_tenant
from app.models import Tenant
from app.schemas import TenantResponse

router = APIRouter(prefix="/tenants", tags=["Tenants"])


@router.get("/current", response_model=TenantResponse)
def get_tenant(tenant: Tenant = Depends(get_current_tenant)):
    return tenant


@router.get("/", response_model=list[TenantResponse])
def list_tenants(db: Session = Depends(get_db)):
    return db.query(Tenant).filter(Tenant.is_active == True).all()