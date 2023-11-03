import enum


class ExchangeOperationType(enum.Enum):
    BUY = 1
    SELL = 2


class CryptoCurrencies(enum.Enum):
    BTC = 1
    USDT = 2
    ETH = 3
    BUSD = 4
    DAI = 5
