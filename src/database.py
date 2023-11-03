import uuid
import sqlalchemy as sa
import datetime as dt
from contextvars import ContextVar
from functools import wraps

from loguru import logger
from sqlalchemy.ext.asyncio import (AsyncSession, async_scoped_session,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import as_declarative

from src import config

METADATA = sa.MetaData()

class GlobalScopeError(Exception):
    pass


session_scope = ContextVar("session_scope", default="global")

engine = create_async_engine(
    config.APP_DB_DSN,
    echo=True,
)

DEFAULT_SESSION_FACTORY = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)
scoped_async_session = async_scoped_session(
    DEFAULT_SESSION_FACTORY, scopefunc=session_scope.get
)


def get_session() -> AsyncSession:
    scope = session_scope.get()
    if scope == "global":
        raise GlobalScopeError
    return scoped_async_session()


class scoped_transaction:
    def __call__(self, func):  # type: ignore
        @wraps(func)
        async def wrap(*args, **kwargs):  # type: ignore[no-untyped-def]
            async with self:
                return await func(*args, **kwargs)

        return wrap

    async def __aenter__(self) -> AsyncSession:
        self.session_id = str(uuid.uuid4())
        self.token = session_scope.set(self.session_id)
        self.session: AsyncSession = scoped_async_session()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore
        if exc_type:
            logger.debug("rollback {}", self.session_id)
            await self.session.rollback()
        else:
            logger.debug("commit {}", self.session_id)
            await self.session.commit()
        await self.session.close()
        await scoped_async_session.remove()
        session_scope.reset(self.token)


@as_declarative(metadata=METADATA)
class AppORM:
    created_at = sa.Column(sa.DateTime(timezone=True), nullable=False, default=dt.datetime.utcnow)
    updated_at = sa.Column(
        sa.DateTime(timezone=True),
        nullable=False,
        default=dt.datetime.utcnow,
        onupdate=dt.datetime.utcnow,
    )
