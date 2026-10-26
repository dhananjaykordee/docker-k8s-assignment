from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from routes.auth_routes import router as auth_router
from routes.booking_routes import router as booking_router
from routes.room_routes import router as room_router
from utils.exception_handler import validation_exception_handler

app = FastAPI(title="Meeting Room Booking API")
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(auth_router)
app.include_router(room_router)
app.include_router(booking_router)
