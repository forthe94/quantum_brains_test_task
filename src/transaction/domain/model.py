import dataclasses
import uuid

from src.exchange import enums
from src.transaction import enums as enums_transaction


@dataclasses.dataclass
class Transaction:
    user_id: uuid.UUID
    amount: float
    operation_type: enums.ExchangeOperationType
    from_currency: enums.CryptoCurrencies
    to_currency: enums.CryptoCurrencies
    rate: float
    status: enums_transaction.TransactionStatus = (
        enums_transaction.TransactionStatus.CREATED
    )
    id: uuid.UUID = dataclasses.field(default_factory=uuid.uuid4)
