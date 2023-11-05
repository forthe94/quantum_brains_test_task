import dataclasses
import uuid
from collections import defaultdict


@dataclasses.dataclass
class User:
    tg_id: int
    balances: defaultdict[str, float] = dataclasses.field(
        default_factory=lambda: defaultdict(float)
    )
    id: uuid.UUID = dataclasses.field(default_factory=uuid.uuid4)


@dataclasses.dataclass
class UserPNL:
    balances: defaultdict[str, float] = dataclasses.field(
        default_factory=lambda: defaultdict(float)
    )
