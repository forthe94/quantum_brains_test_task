import uuid
from collections import defaultdict

import pytest

from src.database import scoped_transaction
from src.exchange import enums
from src.transaction import enums as transaction_enums
from src.transaction.adapters.repository import TransactionRepository
from src.transaction.domain.model import Transaction
from src.user.adapters.repository import UserRepository
from src.user.domain.model import User

pytestmark = pytest.mark.asyncio


async def test_get_completed_transactions(
    clear_db,
) -> None:
    user = User(
        id=uuid.uuid4(), tg_id=1, balances=defaultdict(float, {"BTC": 1.0, "ETH": 3.0})
    )

    user_repo = UserRepository()
    transaction_repo = TransactionRepository()
    async with scoped_transaction():
        await user_repo.create(user)
        for _ in range(10):
            transaction = Transaction(
                user_id=user.id,
                amount=5,
                operation_type=enums.ExchangeOperationType.SELL,
                from_currency=enums.CryptoCurrencies.BTC,
                to_currency=enums.CryptoCurrencies.ETH,
                rate=2.0,
                status=transaction_enums.TransactionStatus.COMPLETED,
            )
            await transaction_repo.create(transaction)
    async with scoped_transaction():
        async for db_trans in transaction_repo.get_completed_transactions(user.id):
            assert db_trans.amount == 5

