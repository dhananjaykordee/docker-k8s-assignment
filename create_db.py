from model.bookings import Booking
from model.user import User
from utils.database import Base, engine, SessionLocal

try:
    Base.metadata.create_all(bind=engine)
    print("Database tables ensured successfully")
except Exception as exc:
    if "already exists" not in str(exc).lower():
        raise
    print("Database tables already exist")

db = SessionLocal()
try:
    existing_user = db.query(User).filter(User.username == "admin").first()

    if not existing_user:
        admin_user = User(
            id=1,
            fullname="Dhananjay Korde",
            username="admin",
            password_hash=(
                "$2b$12$noHzUCnNLZsV6J1VB5PT/"
                "uAlwuHIBMVU4s.uG/cnrifDgigKhiXj6"
            ),
        )
        db.add(admin_user)
        db.commit()
        print("Admin user created successfully")
    else:
        print("Admin user already exists")
finally:
    db.close()
