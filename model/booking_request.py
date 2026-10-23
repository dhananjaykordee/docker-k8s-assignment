from pydantic import BaseModel


class BookingRequest(BaseModel):
    room_id: int
    booking_date: str
    start_time: str
    end_time: str
