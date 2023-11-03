import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from src.transaction import enums as enums_transaction
from src.database import AppORM
from src.exchange import enums


class TransactionORM(AppORM):
    __tablename__ = "transaction"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = sa.Column(sa.Enum(enums_transaction.TransactionStatus))
    user_id = sa.Column(sa.ForeignKey("user.id"), nullable=False)
    operation_type = sa.Column(sa.Enum(enums.ExchangeOperationType))
    from_currency = sa.Column(sa.Enum(enums.CryptoCurrencies))
    to_currency = sa.Column(sa.Enum(enums.CryptoCurrencies))
    rate = sa.Column(sa.Float, nullable=False)
