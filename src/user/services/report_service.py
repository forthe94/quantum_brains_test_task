import asyncio

from src.database import scoped_transaction
from src.exchange import enums
from src.exchange.adapters.rates_client import rates_client
from src.transaction.adapters.repository import TransactionRepository
from src.user.adapters.repository import UserRepository
from src.user.domain.model import User, UserPNL


class UserReportService:
    def __init__(self) -> None:
        self.user_repository = UserRepository()
        self.transaction_repository = TransactionRepository()
        self.rates_client = rates_client

    async def __process_coin(
        self, user_pnl: UserPNL, coin: str, currency: enums.CryptoCurrencies
    ) -> None:
        amount = user_pnl.balances[coin]
        rate = await self.rates_client.get_rates(coin, currency.name)
        if amount > 0:
            # Если больше нуля надо продать
            user_pnl.balances[coin] -= amount
            user_pnl.balances[currency.name] += amount * rate
        else:
            user_pnl.balances[coin] += amount
            user_pnl.balances[currency.name] -= amount * rate

    async def _count_pnl(
        self, user: User, currency: enums.CryptoCurrencies = enums.CryptoCurrencies.BTC
    ) -> float:
        user_pnl = UserPNL()
        async with scoped_transaction():
            async for trans in self.transaction_repository.get_completed_transactions(
                user.id
            ):
                if trans.operation_type == enums.ExchangeOperationType.SELL:
                    user_pnl.balances[trans.from_currency.name] -= trans.amount
                    user_pnl.balances[trans.to_currency.name] += (
                        trans.amount * trans.rate
                    )
                else:
                    user_pnl.balances[trans.from_currency.name] += trans.amount
                    user_pnl.balances[trans.to_currency.name] -= (
                        trans.amount * trans.rate
                    )
        coins_to_convert = (coin for coin in user_pnl.balances if coin != currency.name)
        tasks = []
        for coin in coins_to_convert:
            tasks.append(self.__process_coin(user_pnl, coin, currency))
        await asyncio.gather(*tasks)
        return user_pnl.balances[currency.name]

    async def generate_report(self, user_tg_id: int) -> str:
        ret = ""
        async with scoped_transaction():
            user = await self.user_repository.get(tg_id=user_tg_id)

        for coin_name, coin_val in user.balances.items():
            ret += f"{coin_name}: {coin_val:.6f}\n"
        pnl_coin = enums.CryptoCurrencies.BTC
        pnl = await self._count_pnl(user, pnl_coin)
        ret += f"PNL in {pnl_coin.name}: {pnl:.6f}"
        return ret
