from sqlalchemy import Column, Identity, Integer, String

from utils.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        Identity(),
        primary_key=True,
        index=True,
    )

    fullname = Column(
        String,
        nullable=False,
    )

    username = Column(String, unique=True, nullable=False)

    password_hash = Column(String, nullable=False)
