from app.database import SessionLocal
from app.models import User
from app.security import hash_password
from dotenv import load_dotenv
import os

load_dotenv()

email = os.getenv("SUPERADMIN_EMAIL")
password = os.getenv("SUPERADMIN_PASSWORD")

with SessionLocal() as db:
    admin = db.query(User).filter(User.email == email).first()

    if admin:
        admin.password_hash = hash_password(password)
        admin.role = "super_admin"
        admin.tenant_id = None
        admin.is_active = True
        print("Super Admin password updated.")
    else:
        admin = User(
            name="Super Admin",
            email=email,
            password_hash=hash_password(password),
            role="super_admin",
            tenant_id=None,
            is_active=True,
        )
        db.add(admin)
        print("Super Admin created.")

    db.commit()