import random

from src.exchange import enums
from src.exchange.adapters.rates_client import rates_client


class ExchangeAPIError(Exception):
    pass


class ExchangeApi:
    async def sell(
        self,
        amount: float,
        from_currency: enums.CryptoCurrencies,
        to_currency: enums.CryptoCurrencies,
    ) -> float:
        # Например продать 10 BTC за USDT - тогда курс будет BTC/USDT
        # и количество полученных USDT = количество BTC * rate
        if random.randint(0, 9) == 1:
            raise ExchangeAPIError
        rate = await rates_client.get_rates(from_currency.name, to_currency.name)
        return rate

    async def buy(
        self,
        amount: float,
        from_currency: enums.CryptoCurrencies,
        to_currency: enums.CryptoCurrencies,
    ) -> float:
        # Например купить 10 BTC за USDT - тогда курс будет BTC/USDT
        # и необходимое количество USDT = rate * количество BTC
        if random.randint(0, 9) == 1:
            raise ExchangeAPIError

        rate = await rates_client.get_rates(from_currency.name, to_currency.name)
        return rate


exchange_api = ExchangeApi()
