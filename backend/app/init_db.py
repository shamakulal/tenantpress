from sqlalchemy import select

from app.database import Base, engine, SessionLocal
from app.models import Tenant


def initialize_database():
    Base.metadata.create_all(bind=engine)

    demo_tenants = [
        {
            "name": "Tenant A",
            "slug": "tenant-a",
            "subdomain": "tenant-a",
        },
        {
            "name": "Tenant B",
            "slug": "tenant-b",
            "subdomain": "tenant-b",
        },
        {
            "name": "Tenant C",
            "slug": "tenant-c",
            "subdomain": "tenant-c",
        },
    ]

    with SessionLocal() as db:
        for tenant_data in demo_tenants:
            existing_tenant = db.scalar(
                select(Tenant).where(
                    Tenant.slug == tenant_data["slug"]
                )
            )

            if existing_tenant is None:
                db.add(Tenant(**tenant_data))

        db.commit()

    print("Database tables created.")
    print("Demo tenants inserted or already present.")


if __name__ == "__main__":
    initialize_database()