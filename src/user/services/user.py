from src.user.adapters.repository import UserRepository


class UserService:
    def __init__(self) -> None:
        self.user_repository = UserRepository()
