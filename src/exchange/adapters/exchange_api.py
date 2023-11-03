from src.exchange import enums
from src.exchange.adapters.rates_client import rates_client


class ExchangeApi:
    async def sell(
        self,
        amount: float,
        from_currency: enums.CryptoCurrencies,
        to_currency: enums.CryptoCurrencies,
    ) -> float:
        # Например продать 10 BTC за USDT - тогда курс будет BTC/USDT
        # и количество полученных USDT = количество BTC * rate
        rate = await rates_client.get_rates(from_currency.name, to_currency.name)
        return rate * amount

    async def buy(
        self,
        amount: float,
        from_currency: enums.CryptoCurrencies,
        to_currency: enums.CryptoCurrencies,
    ) -> float:
        # Например купить 10 BTC за USDT - тогда курс будет BTC/USDT
        # и необходимое количество USDT = rate * количество BTC
        rate = await rates_client.get_rates(from_currency.name, to_currency.name)
        return amount * rate


exchange_api = ExchangeApi()
