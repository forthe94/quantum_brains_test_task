import json
import uuid
from collections import defaultdict

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from src.database import AppORM
from src.user.domain.model import User


class UserORM(AppORM):
    __tablename__ = "user"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tg_id = sa.Column(sa.BigInteger, nullable=False)
    balances = sa.Column(sa.JSON, nullable=False)

    def to_domain(self) -> User:
        return User(
            tg_id=self.tg_id,  # type: ignore
            balances=defaultdict(float, json.loads(self.balances)),  # type: ignore
            id=self.id,  # type: ignore
        )


class UserRequestORM(AppORM):
    __tablename__ = "user_reqeust"
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = sa.Column(sa.ForeignKey("user.id"), nullable=False)
    text = sa.Column(sa.Text, nullable=False)
