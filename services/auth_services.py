from repository.user_repository import UserRepository
from auth.password_handler import verify_password
from auth.jwt_handler import create_access_token


class AuthService:

    @staticmethod
    def login(username, password, db):

        user = UserRepository.get_by_username(db, username)

        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        token = create_access_token({"sub": user.username})

        return token

    @staticmethod
    def get_profile(username, db):
        return UserRepository.get_by_username(db, username)
