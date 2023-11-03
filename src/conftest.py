

import pytest_asyncio
from src.database import METADATA, scoped_async_session


@pytest_asyncio.fixture
async def clear_db():
    """
    Clear DataBase after test. Use it in test with neste transactions
    """
    try:
        yield
    finally:
        session = scoped_async_session()
        for tbl in reversed(METADATA.sorted_tables):
            await session.execute(tbl.delete())
        await session.commit()

