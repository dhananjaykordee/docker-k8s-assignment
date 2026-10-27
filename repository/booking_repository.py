from sqlalchemy import func

from model.bookings import Booking


class BookingRepository:

    @staticmethod
    def save(db, booking):
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking

    @staticmethod
    def get_next_id(db):
        return (db.query(func.max(Booking.id)).scalar() or 0) + 1

    @staticmethod
    def get_all_by_user(db, username):
        return db.query(Booking).filter(Booking.username == username).all()

    @staticmethod
    def get_all_by_room(db, room_id):
        return db.query(Booking).filter(Booking.room_id == room_id).all()

    @staticmethod
    def get_by_id(db, booking_id):
        return db.query(Booking).filter(Booking.id == booking_id).first()

    @staticmethod
    def get_room_bookings(db, room_id, booking_date):
        return (
            db.query(Booking)
            .filter(
                Booking.room_id == room_id,
                Booking.booking_date == booking_date,
                Booking.status == "BOOKED",
            )
            .all()
        )

    @staticmethod
    def cancel_booking(db, booking):
        booking.status = "CANCELLED"
        db.commit()
        db.refresh(booking)
        return booking
