from app.db.database import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.models.tenant import Tenant
from app.core.security import get_password_hash  # assuming you have a hashing function

def create_admin():
    db = SessionLocal()

    # Create default tenant
    tenant = db.query(Tenant).filter_by(name="DefaultTenant").first()
    if not tenant:
        tenant = Tenant(name="DefaultTenant", address="N/A")
        db.add(tenant)
        db.commit()
        db.refresh(tenant)

    # Create admin role
    admin_role = db.query(Role).filter_by(name="admin").first()
    if not admin_role:
        admin_role = Role(name="admin")
        db.add(admin_role)
        db.commit()
        db.refresh(admin_role)

    # Create admin user
    admin_user = db.query(User).filter_by(username="admin").first()
    if not admin_user:
        print("tenant object", tenant)
       
        admin_user = User(
            username="admin",
            full_name="System Admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            is_superuser=True,
            tenant_id=tenant.id
        )
        admin_user.roles.append(admin_role)  # ✅ this will now work

        db.add(admin_user)
        db.commit()
        print("Admin user created successfully.")
    else:
        print("Admin user already exists.")

    db.close()

if __name__ == "__main__":
    create_admin()
