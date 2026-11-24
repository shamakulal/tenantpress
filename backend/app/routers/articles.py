from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_tenant, require_tenant_access, get_current_user
from app.models import Article, Tenant, User
from app.schemas import ArticleCreate, ArticleResponse

router = APIRouter(prefix="/articles", tags=["Articles"])


@router.get("/", response_model=list[ArticleResponse])
def list_articles(
    tenant: Tenant = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    return db.query(Article).filter(
        Article.tenant_id == tenant.id,
        Article.status == "published"
    ).all()


@router.get("/{article_id}", response_model=ArticleResponse)
def get_article(
    article_id: int,
    tenant: Tenant = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    article = db.query(Article).filter(
        Article.id == article_id,
        Article.tenant_id == tenant.id,
        Article.status == "published"
    ).first()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    return article


@router.post("/", response_model=ArticleResponse)
def create_article(
    data: ArticleCreate,
    tenant: Tenant = Depends(require_tenant_access),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user.role not in ("tenant_admin", "super_admin"):
        raise HTTPException(status_code=403, detail="Admin access required")

    article = Article(
        **data.model_dump(),
        tenant_id=tenant.id,
        author_id=user.id
    )

    db.add(article)
    db.commit()
    db.refresh(article)
    return article


@router.put("/{article_id}", response_model=ArticleResponse)
def update_article(
    article_id: int,
    data: ArticleCreate,
    tenant: Tenant = Depends(require_tenant_access),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user.role not in ("tenant_admin", "super_admin"):
        raise HTTPException(status_code=403, detail="Admin access required")

    article = db.query(Article).filter(
        Article.id == article_id,
        Article.tenant_id == tenant.id
    ).first()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    for key, value in data.model_dump().items():
        setattr(article, key, value)

    db.commit()
    db.refresh(article)
    return article


@router.delete("/{article_id}")
def delete_article(
    article_id: int,
    tenant: Tenant = Depends(require_tenant_access),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user.role not in ("tenant_admin", "super_admin"):
        raise HTTPException(status_code=403, detail="Admin access required")

    article = db.query(Article).filter(
        Article.id == article_id,
        Article.tenant_id == tenant.id
    ).first()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    db.delete(article)
    db.commit()
    return {"message": "Article deleted"}