import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from src.database import AppORM


class UserORM(AppORM):
    __tablename__ = "user_profiles"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tg_id = sa.Column(sa.BigInteger, nullable=False)
    balances = sa.Column(sa.JSON, nullable=False)
