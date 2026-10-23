from model.user import User


class UserRepository:

    @staticmethod
    def get_by_username(db, username):
        return db.query(User).filter(User.username == username).first()
