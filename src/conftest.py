import asyncio
import datetime
import time
import uuid
from typing import Any, Callable

import pytest
import pytest_asyncio
from src.database import DBMetadata, scoped_async_session, session_scope


@pytest.fixture
async def clear_db():
    """
    Clear DataBase after test. Use it in test with neste transactions
    """
    try:
        yield
    finally:
        session = scoped_async_session()
        for tbl in reversed(DBMetadata.metadata.sorted_tables):
            await session.execute(tbl.delete())
        await session.commit()

