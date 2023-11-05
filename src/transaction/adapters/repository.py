import uuid
from typing import AsyncGenerator

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session, json_dumps
from src.transaction import enums
from src.transaction.adapters.orm import TransactionORM
from src.transaction.domain.model import Transaction


class TransactionRepository:
    @property
    def session(self) -> AsyncSession:
        return get_session()

    async def create(self, transaction: Transaction) -> None:
        q = sa.insert(TransactionORM).values(
            id=transaction.id,
            amount=transaction.amount,
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
        q = (
            sa.update(TransactionORM)
            .where(TransactionORM.id == transaction_id)
            .values(status=status)
        )

        await self.session.execute(q)

    async def get_completed_transactions(
        self, user_id: uuid.UUID, batch_size: int = 50
    ) -> AsyncGenerator[Transaction, None]:
        q = sa.select(TransactionORM).where(
            TransactionORM.user_id == user_id,
            TransactionORM.status == enums.TransactionStatus.COMPLETED,
        )
        result = await self.session.stream(
            q, execution_options={"yield_per": batch_size}
        )
        async for row in result:
            orm = row[0]
            yield Transaction(
                user_id=orm.user_id,
                amount=orm.amount,
                operation_type=orm.operation_type,
                from_currency=orm.from_currency,
                to_currency=orm.to_currency,
                rate=orm.rate,
                status=orm.status,
                id=orm.id,
            )
