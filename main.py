import asyncio
import logging

from aiogram_dialog.api.exceptions import UnknownIntent
from aiogram import Dispatcher, Router, F
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ErrorEvent, ReplyKeyboardRemove
from aiogram.exceptions import TelegramBadRequest

from aiogram_dialog import (
    DialogManager, setup_dialogs, StartMode, ShowMode,
)

from bot import states
from bot.auth_2 import auth_dialog_2
from bot.auth_1 import auth_dialog_1
from bot.choise import choise_dialog
from bot.main_dialog import main_dialog
from bot.platform_2 import platfrom_dialog_2
from bot.platform_1 import platfrom_dialog_1

from BOT import bot


async def start(message: Message, dialog_manager: DialogManager):
    # it is important to reset stack because user wants to restart everything
    await dialog_manager.start(states.MainState.MAIN, mode=StartMode.RESET_STACK)

async def reviews(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(states.MainState.REVIEWS, mode=StartMode.RESET_STACK)


async def on_unknown_intent(event: ErrorEvent, dialog_manager: DialogManager):
    # Example of handling UnknownIntent Error and starting new dialog.
    logging.error("Restarting dialog: %s", event.exception)
    if event.update.callback_query:
        await event.update.callback_query.answer(
            "Bot process was restarted due to maintenance.\n"
            "Redirecting to main menu.",
        )
        if event.update.callback_query.message:
            try:
                await event.update.callback_query.message.delete()
            except TelegramBadRequest:
                pass  # whatever
    elif event.update.message:
        await event.update.message.answer(
            "Bot process was restarted due to maintenance.\n"
            "Redirecting to main menu.",
            reply_markup=ReplyKeyboardRemove(),
        )
    await dialog_manager.start(
        states.MainState.MAIN,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )


dialog_router = Router()
dialog_router.include_routers(
    main_dialog,
    choise_dialog,
    platfrom_dialog_1,
    platfrom_dialog_2,
    auth_dialog_1,
    auth_dialog_2
)


def setup_dp():
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.message.register(start, F.text == "/start")
    dp.message.register(reviews, F.text == "/reviews")
    dp.errors.register(
        on_unknown_intent,
        ExceptionTypeFilter(UnknownIntent),
    )
    dp.include_router(dialog_router)
    setup_dialogs(dp)
    return dp


async def main(bot):
    # real main
    logging.basicConfig(level=logging.INFO)
    dp = setup_dp()
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main(bot))
