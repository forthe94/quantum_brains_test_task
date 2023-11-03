import enum


class TransactionStatus(enum.Enum):
    CREATED = 1
    COMPLETED = 2
    REJECTED = 3
