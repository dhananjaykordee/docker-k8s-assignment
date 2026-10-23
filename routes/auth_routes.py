from fastapi import APIRouter, Depends, HTTPException

from model.login_request import LoginRequest
from services.auth_services import AuthService
from utils.database import get_db

from auth.auth_dependency import get_current_user

router = APIRouter()


@router.post("/login")
def login(request: LoginRequest, db=Depends(get_db)):
    token = AuthService.login(request.username, request.password, db)

    if not token:
        raise HTTPException(
            status_code=401, detail="Invalid username or password"
        )

    return {"access_token": token, "token_type": "Bearer"}


@router.get("/profile")
def profile(username=Depends(get_current_user), db=Depends(get_db)):
    user = AuthService.get_profile(username, db)

    return {"fullname": user.fullname, "username": user.username}
