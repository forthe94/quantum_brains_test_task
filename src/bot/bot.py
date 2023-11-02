from aiogram import Bot, Dispatcher, types
from loguru import logger

from src import config

bot = Bot(token=config.BOT_TOKEN)
dispatcher = Dispatcher(bot=bot)


@dispatcher.message_handler(commands="start")
async def entry_point(
    message: types.Message,
) -> None:
    return


# @dispatcher.message_handler()


async def start_app() -> None:
    logger.info("Start app quantum brains exchange")
    try:
        await dispatcher.start_polling()
    finally:
        await (await bot.get_session()).close()
