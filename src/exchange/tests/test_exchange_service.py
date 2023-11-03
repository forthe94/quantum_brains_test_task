import json
from collections import defaultdict

from src.database import scoped_transaction
from src.exchange import enums
from src.exchange.services.exchange import ExchangeService
from src.user.adapters.orm import UserORM
from src.user.adapters.repository import UserRepository
from src.user.domain.model import User
import pytest
import sqlalchemy as sa

pytestmark = pytest.mark.asyncio


async def test_sell_exchange(
    rates_service_mock,
    clear_db,
):
    exchange_service = ExchangeService()
    user_repository = UserRepository()
    tg_id = 12345
    async with scoped_transaction():
        await user_repository.create(
            user=User(
                tg_id=tg_id,
                balances=defaultdict(float, {enums.CryptoCurrencies.BTC.name: 10.0}),
            )
        )

    await exchange_service.process_exchange(
        tg_id,
        operation_type=enums.ExchangeOperationType.SELL,
        amount=5,
        from_currency=enums.CryptoCurrencies.BTC,
        to_currency=enums.CryptoCurrencies.ETH,
    )

    async with scoped_transaction() as session:
        result = (await session.execute(sa.select(UserORM))).scalars().first()

    balances = json.loads(result.balances)

    assert balances["BTC"] == 5.0
    assert balances["ETH"] == 10.0
