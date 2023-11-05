from collections import defaultdict

from src.database import scoped_transaction
from src.user.adapters.repository import UserRepository, UserRequestRepository
from src.user.domain.model import User


class UserService:
    def __init__(self) -> None:
        self.user_repository = UserRepository()
        self.user_request_repository = UserRequestRepository()

    async def create_new_user(
        self, tg_id: int, balances=defaultdict(float, {})
    ) -> None:
        user = User(tg_id=tg_id, balances=balances)
        await self.user_repository.create(user)

    async def add_user_request(self, tg_id: int, text: str) -> None:
        async with scoped_transaction():
            user = await self.user_repository.get(tg_id=tg_id)

            await self.user_request_repository.create(user_id=user.id, text=text)
