from src.database import scoped_transaction
from src.transaction.adapters.repository import TransactionRepository
from src.user.adapters.repository import UserRepository


class UserReportService:
    def __init__(self) -> None:
        self.user_repository = UserRepository()
        self.transaction_repository = TransactionRepository()

    async def generate_report(self, user_tg_id: int) -> str:
        ret = ""
        async with scoped_transaction():
            user = await self.user_repository.get(tg_id=user_tg_id)

        for coin_name, coin_val in user.balances.items():
            ret += f"{coin_name}: {coin_val}\n"

        return ret
