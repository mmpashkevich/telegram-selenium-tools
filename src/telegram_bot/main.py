
import asyncio
import base64
import logging
import os
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, BufferedInputFile
from src.selenium_service.models import SeleniumApiForecaImage
from src.telegram_bot.telegram_service import TelegramService

# TODO: make logging according to best practices

# Bot token can be obtained via https://t.me/BotFather
TOKEN = os.getenv("TELEGRAM_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()
telegram_service = TelegramService()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    print('start')
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        foreca_image: SeleniumApiForecaImage = telegram_service.get_foreca_image()
        if foreca_image is None:
            await message.answer("Error get weather picture. Try through few minutes.")
            return

        photo_bytes: bytes = base64.b64decode(foreca_image.image_base64)
        photo: BufferedInputFile = BufferedInputFile(photo_bytes,
                                                     foreca_image.name,
                                                     )
        await message.answer_photo(photo, caption=foreca_image.name)

    except Exception as err:
        logging.error(err)
        await message.answer("Sorry. Error. I'm sorry, but I can't do that.")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())