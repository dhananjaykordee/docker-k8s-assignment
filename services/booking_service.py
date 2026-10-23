from datetime import datetime

from model.bookings import Booking
from repository.booking_repository import BookingRepository
from services.room_services import RoomService


class BookingServiceError(Exception):
    pass


def _time_to_minutes(value, allow_midnight_end=False):
    if value == "24:00" and allow_midnight_end:
        return 24 * 60

    try:
        parsed_time = datetime.strptime(value, "%H:%M")
    except ValueError as exc:
        raise BookingServiceError(
            "Times must use 24-hour HH:MM format; 24:00 is allowed "
            "only as an end time"
        ) from exc

    if parsed_time.strftime("%H:%M") != value:
        raise BookingServiceError(
            "Times must use 24-hour HH:MM format; 24:00 is allowed "
            "only as an end time"
        )

    return parsed_time.hour * 60 + parsed_time.minute


class BookingService:

    @staticmethod
    def book_room(request, username, db):

        room = RoomService.get_room_by_id(request.room_id)

        if not room:
            raise BookingServiceError("Room not found")

        new_start = _time_to_minutes(request.start_time)
        new_end = _time_to_minutes(
            request.end_time,
            allow_midnight_end=True,
        )

        if new_start >= new_end:
            raise BookingServiceError("Start time must be before end time")

        existing_bookings = BookingRepository.get_room_bookings(
            db, request.room_id, request.booking_date
        )

        for booking in existing_bookings:

            existing_start = _time_to_minutes(booking.start_time)
            existing_end = _time_to_minutes(
                booking.end_time,
                allow_midnight_end=True,
            )

            if new_start < existing_end and new_end > existing_start:
                raise BookingServiceError(
                    "Room already booked for selected slot"
                )

        booking = Booking(
            id=BookingRepository.get_next_id(db),
            room_id=request.room_id,
            username=username,
            booking_date=request.booking_date,
            start_time=request.start_time,
            end_time=request.end_time,
            status="BOOKED",
        )

        return BookingRepository.save(db, booking)

    @staticmethod
    def get_user_bookings(username, db):
        return BookingRepository.get_all_by_user(db, username)

    @staticmethod
    def get_booking(booking_id, db):
        return BookingRepository.get_by_id(db, booking_id)

    @staticmethod
    def cancel_booking(booking_id, username, db):

        booking = BookingRepository.get_by_id(db, booking_id)

        if not booking:
            raise BookingServiceError("Booking not found")

        if booking.username != username:
            raise BookingServiceError("You can cancel only your own bookings")

        if booking.status == "CANCELLED":
            raise BookingServiceError("Booking already cancelled")

        return BookingRepository.cancel_booking(db, booking)
