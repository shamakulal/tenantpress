import os

from app.database import SessionLocal
from app.models import User
from app.security import hash_password


def create_super_admin():
    email = os.getenv("SUPERADMIN_EMAIL")
    password = os.getenv("SUPERADMIN_PASSWORD")

    if not email or not password:
        raise ValueError(
            "Set SUPERADMIN_EMAIL and SUPERADMIN_PASSWORD in .env first"
        )

    with SessionLocal() as db:
        existing = db.query(User).filter(User.email == email).first()

        if existing:
            print("Super Admin already exists.")
            return

        admin = User(
            tenant_id=None,
            name="Super Admin",
            email=email,
            password_hash=hash_password(password),
            role="super_admin",
            is_active=True,
        )

        db.add(admin)
        db.commit()

    print("Super Admin created successfully.")


if __name__ == "__main__":
    create_super_admin()