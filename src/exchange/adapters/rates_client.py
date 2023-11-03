from typing import Any

import httpx

from src import config


class RatesClient:
    def __init__(self) -> None:
        self._cli = httpx.AsyncClient(
            base_url=f"{config.RATES_API_HOST}",
            headers={"X-Api-Key": config.RATES_API_KEY},
            timeout=5,
            verify=False,
        )

    async def get_rates(self, from_currency: str, to_currency: str) -> float:
        """

        :param symbol: Пара валют для обмена в формате "BTCUSDT"
        :return: '{"symbol": "BTCUSDT", "price": "34489.50000000", "timestamp": 1698995976}'
        """
        resp = await self._cli.get(
            f"/cryptoprice", params={"symbol": from_currency + to_currency}
        )
        if resp.status_code == 400:
            resp = await self._cli.get(
                f"/cryptoprice", params={"symbol": to_currency + from_currency}
            )
            val = 1 / float(resp.json()["price"])
        else:
            val = float(resp.json()["price"])
        resp.raise_for_status()
        return val

    async def close(self) -> None:
        await self._cli.aclose()


rates_client = RatesClient()
