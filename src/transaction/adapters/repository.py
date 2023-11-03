import uuid

import sqlalchemy as sa

from src.database import get_session, json_dumps
from src.transaction import enums
from src.transaction.adapters.orm import TransactionORM
from src.transaction.domain.model import Transaction
from sqlalchemy.ext.asyncio import AsyncSession


class TransactionRepository:
    @property
    def session(self) -> AsyncSession:
        return get_session()

    async def create(self, transaction: Transaction) -> None:
        q = sa.insert(TransactionORM).values(
            id=transaction.id,
            user_id=transaction.user_id,
            operation_type=transaction.operation_type,
            from_currency=transaction.from_currency,
            to_currency=transaction.to_currency,
            status=transaction.status,
            rate=transaction.rate,
        )

        await self.session.execute(q)

    async def update_status(
        self, transaction_id: uuid.UUID, status: enums.TransactionStatus
    ) -> None:
        q = sa.update(TransactionORM).where(TransactionORM.id==transaction_id).values(status=status)

        await self.session.execute(q)
