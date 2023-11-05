from collections import defaultdict

from src.user.adapters.repository import UserRepository
from src.user.domain.model import User


class UserService:
    def __init__(self) -> None:
        self.user_repository = UserRepository()

    async def create_new_user(
        self, tg_id: int, balances=defaultdict(float, {})
    ) -> None:
        user = User(tg_id=tg_id, balances=balances)
        await self.user_repository.create(user)
