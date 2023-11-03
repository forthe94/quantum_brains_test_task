from aiogram import Bot, Dispatcher, types
from loguru import logger

from src import config
from src.database import scoped_transaction
from src.user.services.user import UserService

bot = Bot(token=config.BOT_TOKEN)
dispatcher = Dispatcher(bot=bot)


@dispatcher.message_handler(commands="start")
async def entry_point(
    message: types.Message,
) -> None:
    user_service = UserService()
    async with scoped_transaction():
        await user_service.create_new_user(message.from_user.id)


# @dispatcher.message_handler()


async def start_app() -> None:
    logger.info("Start app quantum brains exchange")
    try:
        await dispatcher.start_polling()
    finally:
        await (await bot.get_session()).close()
