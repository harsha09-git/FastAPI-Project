from app.database import SessionLocal, engine, Base
from app.models import User, Role
from app.core.security import hash_password
from app.utils.permissions import seed_roles_permissions

Base.metadata.create_all(bind=engine)

db = SessionLocal()

seed_roles_permissions(db)

admin_role = db.query(Role).filter_by(name="admin").first()

if not admin_role:
    print("Admin role not found!")
    exit()

existing_user = db.query(User).filter_by(email="admin@example.com").first()

if existing_user:
    print("User already exists!")
else:
    admin_user = User(
        email="admin@example.com",
        hashed_password=hash_password("admin123"),
        role_id=admin_role.id
    )
    db.add(admin_user)
    db.commit()
    print("Admin user created successfully!")
    print("Email: admin@example.com")
    print("Password: admin123")

db.close()