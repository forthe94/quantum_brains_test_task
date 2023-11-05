import uuid

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session, json_dumps
from src.user.adapters.orm import UserORM
from src.user.domain.model import User


class UserRepository:
    @property
    def session(self) -> AsyncSession:
        return get_session()

    async def create(self, user: User) -> None:
        balances = json_dumps(user.balances)
        q = sa.insert(UserORM).values(
            id=user.id,
            tg_id=user.tg_id,
            balances=balances,
        )

        await self.session.execute(q)

    async def get(self, tg_id: int, with_for_update: bool | None = None) -> User:
        q = sa.select(UserORM).where(UserORM.tg_id == tg_id)
        if with_for_update:
            q = q.with_for_update()
        res = await self.session.execute(q)
        user: UserORM = res.scalars().first()

        return user.to_domain()

    async def update_balances(
        self, user_id: uuid.UUID, balances: dict[str, float]
    ) -> None:
        balances_str = json_dumps(balances)

        q = (
            sa.update(UserORM)
            .where(UserORM.id == user_id)
            .values(balances=balances_str)
        )

        await self.session.execute(q)
