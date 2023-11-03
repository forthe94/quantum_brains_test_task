from collections import defaultdict

from aiogram import Bot, Dispatcher, types, filters
from loguru import logger

from src import config
from src.database import scoped_transaction
from src.exchange import enums
from src.exchange.services.exchange import ExchangeService
from src.user.services.user import UserService

bot = Bot(token=config.BOT_TOKEN)
dispatcher = Dispatcher(bot=bot)


@dispatcher.message_handler(commands="start")
async def entry_point(
    message: types.Message,
) -> None:
    user_service = UserService()
    async with scoped_transaction():
        await user_service.create_new_user(message.from_user.id, balances=defaultdict(float, {"BTC": 100}))


def parse_exchange_message(
    text: str,
) -> tuple[
    enums.ExchangeOperationType, float, enums.CryptoCurrencies, enums.CryptoCurrencies
]:
    op, amount, currencies = text.split(" ")
    from_cur, to_cur = currencies.split("/")
    from_cur_enum = enums.CryptoCurrencies[from_cur.upper()]
    to_cur_enum = enums.CryptoCurrencies[to_cur.upper()]
    op_enum = enums.ExchangeOperationType[op.upper()]
    return op_enum, float(amount), from_cur_enum, to_cur_enum


@dispatcher.message_handler(filters.Text(startswith="sell"))
@dispatcher.message_handler(filters.Text(startswith="buy"))
async def exchange_handler(
    message: types.Message,
) -> None:
    exchange_service = ExchangeService()
    try:
        op, amount, from_cur, to_cur = parse_exchange_message(message.text)
    except Exception:
        await message.answer("Wrong command format")
        return

    await exchange_service.process_exchange(
        message.from_user.id, op, amount, from_cur, to_cur
    )
    await message.answer("Exchange successful!")


async def start_app() -> None:
    logger.info("Start app quantum brains exchange")
    try:
        await dispatcher.start_polling()
    finally:
        await (await bot.get_session()).close()
