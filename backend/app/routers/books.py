from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_tenant, require_tenant_access, get_current_user
from app.models import Book, Tenant, User
from app.schemas import BookCreate, BookResponse

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=list[BookResponse])
def list_books(
    tenant: Tenant = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    return db.query(Book).filter(
        Book.tenant_id == tenant.id,
        Book.status == "published"
    ).all()


@router.get("/{book_id}", response_model=BookResponse)
def get_book(
    book_id: int,
    tenant: Tenant = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    book = db.query(Book).filter(
        Book.id == book_id,
        Book.tenant_id == tenant.id,
        Book.status == "published"
    ).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@router.post("/", response_model=BookResponse)
def create_book(
    data: BookCreate,
    tenant: Tenant = Depends(require_tenant_access),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user.role not in ("tenant_admin", "super_admin"):
        raise HTTPException(status_code=403, detail="Admin access required")

    book = Book(
        **data.model_dump(),
        tenant_id=tenant.id,
        author_id=user.id
    )

    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    data: BookCreate,
    tenant: Tenant = Depends(require_tenant_access),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user.role not in ("tenant_admin", "super_admin"):
        raise HTTPException(status_code=403, detail="Admin access required")

    book = db.query(Book).filter(
        Book.id == book_id,
        Book.tenant_id == tenant.id
    ).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in data.model_dump().items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    tenant: Tenant = Depends(require_tenant_access),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user.role not in ("tenant_admin", "super_admin"):
        raise HTTPException(status_code=403, detail="Admin access required")

    book = db.query(Book).filter(
        Book.id == book_id,
        Book.tenant_id == tenant.id
    ).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    return {"message": "Book deleted"}