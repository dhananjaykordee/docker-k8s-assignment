from sqlalchemy import Column, Identity, Integer, String

from utils.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(
        Integer,
        Identity(),
        primary_key=True,
        index=True,
    )
    room_id = Column(Integer, nullable=False)
    username = Column(String, nullable=False)
    booking_date = Column(String, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    status = Column(String, default="BOOKED", nullable=False)
