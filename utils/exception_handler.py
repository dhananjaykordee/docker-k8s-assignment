import logging

from fastapi import Request
from fastapi.exception_handlers import (
    request_validation_exception_handler as default_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    error_locations = [error.get("loc", ()) for error in exc.errors()]
    logger.error("Request validation failed at: %s", error_locations)
    return await default_validation_exception_handler(request, exc)
