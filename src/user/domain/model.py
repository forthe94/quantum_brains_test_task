import dataclasses
import uuid


@dataclasses.dataclass
class User:
    tg_id: int
    balances: dict[str, float]
    id: uuid.UUID = uuid.uuid4()

@dataclasses.dataclass
class UserAccount:
    user_id: uuid.UUID
    id: uuid.UUID = uuid.uuid4()
