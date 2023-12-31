from src.database import scoped_transaction
from src.exchange import enums
from src.exchange.adapters.exchange_api import ExchangeAPIError, exchange_api
from src.exchange.adapters.rates_client import rates_client
from src.transaction import enums as enums_transaction
from src.transaction.adapters.repository import TransactionRepository
from src.transaction.domain.model import Transaction
from src.user.adapters.repository import UserRepository


class ExchangeError(Exception):
    pass


class InsufficientFundsError(ExchangeError):
    pass


class ExchangeFailed(ExchangeError):
    pass


class ExchangeService:
    def __init__(self) -> None:
        self.rates_client = rates_client
        self.exchange_api = exchange_api
        self.user_repository = UserRepository()
        self.transaction_repository = TransactionRepository()

    async def _process_sell(
        self,
        tg_id: int,
        amount: float,
        from_currency: enums.CryptoCurrencies,
        to_currency: enums.CryptoCurrencies,
        transaction: Transaction,
    ) -> float:
        async with scoped_transaction():
            user = await self.user_repository.get(tg_id=tg_id, with_for_update=True)
            # обработка продажи
            # нужно посмотреть что есть остаток для продажи
            if user.balances[from_currency.name] < amount:
                raise InsufficientFundsError

            rate = await self.exchange_api.sell(
                amount, from_currency, to_currency
            )

            user.balances[from_currency.name] -= amount
            user.balances[to_currency.name] += rate * amount
            await self.user_repository.update_balances(user.id, user.balances)
            await self.transaction_repository.update_status(
                transaction.id, enums_transaction.TransactionStatus.COMPLETED
            )
            return rate

    async def _process_buy(
        self,
        tg_id: int,
        amount: float,
        from_currency: enums.CryptoCurrencies,
        to_currency: enums.CryptoCurrencies,
        transaction: Transaction,
        rate: float,
    ) -> float:
        async with scoped_transaction():
            user = await self.user_repository.get(tg_id=tg_id, with_for_update=True)

            buy_amount = amount * rate
            if user.balances[to_currency.name] < buy_amount:
                raise InsufficientFundsError

            rate = await self.exchange_api.buy(
                amount, from_currency, to_currency
            )
            user.balances[from_currency.name] += amount
            user.balances[to_currency.name] -= rate * amount
            await self.user_repository.update_balances(user.id, user.balances)
            await self.transaction_repository.update_status(
                transaction.id, enums_transaction.TransactionStatus.COMPLETED
            )
            return rate

    async def process_exchange(
        self,
        tg_id: int,
        operation_type: enums.ExchangeOperationType,
        amount: float,
        from_currency: enums.CryptoCurrencies,
        to_currency: enums.CryptoCurrencies,
    ) -> float:
        rate = await self.rates_client.get_rates(from_currency.name, to_currency.name)

        async with scoped_transaction():
            user = await self.user_repository.get(tg_id=tg_id)
            transaction = Transaction(
                user_id=user.id,
                amount=amount,
                operation_type=operation_type,
                from_currency=from_currency,
                to_currency=to_currency,
                rate=rate,
            )
            await self.transaction_repository.create(transaction)

        try:
            if operation_type is enums.ExchangeOperationType.SELL:
                rate = await self._process_sell(
                    tg_id, amount, from_currency, to_currency, transaction
                )

            else:
                # Обработка покупки
                rate = await self._process_buy(
                    tg_id, amount, from_currency, to_currency, transaction, rate
                )
        except ExchangeAPIError:
            async with scoped_transaction():
                await self.transaction_repository.update_status(
                    transaction.id, enums_transaction.TransactionStatus.REJECTED
                )
            raise ExchangeFailed
        return rate
