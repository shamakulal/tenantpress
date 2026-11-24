from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import tenants, users, articles, books

app = FastAPI(title="TenantPress API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "TenantPress API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


app.include_router(tenants.router)
app.include_router(users.router)
app.include_router(articles.router)
app.include_router(books.router)