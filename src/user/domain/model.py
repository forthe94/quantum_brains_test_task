import dataclasses
import uuid


@dataclasses.dataclass
class User:
    id: uuid.UUID
    tg_id: int
    balances: dict[str, float]


@dataclasses.dataclass
class UserAccount:
    id: uuid.UUID
    user_id: uuid.UUID
