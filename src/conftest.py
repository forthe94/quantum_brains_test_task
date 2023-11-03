import asyncio

import pytest_asyncio
import pytest
from src.database import METADATA, scoped_async_session, scoped_transaction


@pytest.yield_fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def clear_db(event_loop):
    """
    Clear DataBase after test. Use it in test with neste transactions
    """
    try:
        yield
    finally:
        async with scoped_transaction() as session:
            for tbl in reversed(METADATA.sorted_tables):
                await session.execute(tbl.delete())


@pytest_asyncio.fixture
async def rates_service_mock(mocker):
    mocker.patch(
        f"src.exchange.adapters.rates_client.RatesClient.get_rates", return_value=2.0
    )
