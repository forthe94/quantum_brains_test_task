import json

import sqlalchemy as sa

from src.database import get_session
from src.user.adapters.orm import UserORM
from src.user.domain.model import User
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    @property
    def session(self):
        return get_session()

    async def create(self, user: User) -> None:
        balances = json.dumps(user.balances)
        q = sa.insert(UserORM).values(
            id=user.id,
            tg_id=user.tg_id,
            balances=balances,
        )

        await self.session.execute(q)
