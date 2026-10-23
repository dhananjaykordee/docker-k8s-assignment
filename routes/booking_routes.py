from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from auth.auth_dependency import get_current_user
from model.booking_request import BookingRequest
from services.booking_service import BookingService, BookingServiceError
from utils.database import get_db

router = APIRouter()


@router.post("/book-room")
def book_room(
    request: BookingRequest,
    username=Depends(get_current_user),
    db=Depends(get_db),
):

    try:
        booking = BookingService.book_room(request, username, db)

        return {
            "booking_id": booking.id,
            "message": "Room booked successfully",
        }

    except BookingServiceError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.get("/my-bookings")
def my_bookings(username=Depends(get_current_user), db=Depends(get_db)):
    return BookingService.get_user_bookings(username, db)


@router.get("/booking/{booking_id}")
def get_booking(
    booking_id: int, username=Depends(get_current_user), db=Depends(get_db)
):
    booking = BookingService.get_booking(booking_id, db)

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    return booking


@router.delete("/booking/{booking_id}")
def cancel_booking(
    booking_id: int, username=Depends(get_current_user), db=Depends(get_db)
):
    try:
        booking = BookingService.cancel_booking(booking_id, username, db)

        return {
            "message": "Booking cancelled successfully",
            "booking_id": booking.id,
        }

    except BookingServiceError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
