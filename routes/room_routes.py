from fastapi import APIRouter, Depends, HTTPException

from services.room_services import RoomService
from auth.auth_dependency import get_current_user

router = APIRouter()


@router.get("/rooms")
def get_rooms(username=Depends(get_current_user)):
    return RoomService.get_rooms()


@router.get("/rooms/{room_id}")
def get_room(room_id: int, username=Depends(get_current_user)):

    room = RoomService.get_room_by_id(room_id)

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    return room
