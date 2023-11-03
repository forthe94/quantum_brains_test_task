import json
import uuid
from collections import defaultdict

import pytest
import sqlalchemy as sa

from src.database import scoped_transaction
from src.user.adapters.orm import UserORM
from src.user.adapters.repository import UserRepository
from src.user.domain.model import User

pytestmark = pytest.mark.asyncio


async def test_create_user(
    clear_db,
) -> None:
    user = User(
        id=uuid.uuid4(), tg_id=1, balances=defaultdict(float, {"BTC": 1.0, "ETH": 3.0})
    )

    user_repo = UserRepository()

    async with scoped_transaction():
        await user_repo.create(user)

    async with scoped_transaction() as session:
        result = (await session.execute(sa.select(UserORM))).scalars().first()

    balances = json.loads(result.balances)
    assert balances["BTC"] == 1.0
    assert balances["ETH"] == 3.0
