from typing import Dict

from aiogram.types import CallbackQuery, InputFile, FSInputFile, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_dialog import Dialog, LaunchMode, Window, DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.kbd import Start, Button, Back, Row, Group, SwitchTo, Cancel, Column
from aiogram_dialog.widgets.text import Const, Format
from . import states

from parse_data import export_admins, create_log_pass_txt
from parse_data import get_reviews, get_last_five_reviews


async def dialog_get_data(dialog_manager: DialogManager, **kwargs):
    user_id = kwargs.get('event_from_user').id

    data = {
        'admins': export_admins(),
        'user_id': user_id,
    }

    return data

async def exit_dialog(callback: CallbackQuery, button: Button, manager: DialogManager, ):
    pass

async def get_five_reviews(callback: CallbackQuery, button: Button,
                           manager: DialogManager):
    reviews = get_last_five_reviews()

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
            text="Назад", callback_data='Start')
    )

    counter = 0
    msg = ''

    for review in range(len(reviews)):
        msg += f'''
<b>Пользователь:</b> {reviews[review][counter]}
<b>Дата отзыва:</b> {reviews[review][counter + 1]}

<b>Текст:</b>

<i>{reviews[review][counter + 2]}</i>

''' + '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^' + '\n'

    await callback.message.answer(msg, parse_mode='HTML', reply_markup=builder.as_markup())


async def get_all_reviews(callback: CallbackQuery, button: Button,
                          manager: DialogManager):
    reviews = get_reviews()

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="Назад", callback_data='Start')
    )

    counter = 0
    msg = ''

    for review in range(len(reviews)):
        msg += f'''
<b>Пользователь:</b> {reviews[review][counter]}
<b>Дата отзыва:</b> {reviews[review][counter + 1]}

<b>Текст:</b>

<i>{reviews[review][counter + 2]}</i>

''' + '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^' + '\n'

    await callback.message.answer(msg, parse_mode='HTML', reply_markup=builder.as_markup())

async def get_photos(callback: CallbackQuery, button: Button,
                          manager: DialogManager):
    await callback.message.answer_photo(IMG_1)
    await callback.message.answer_photo(IMG_2)
    await callback.message.answer_photo(IMG_3)

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="Назад", callback_data='Start')
    )

    await callback.message.answer('💰💰💰', reply_markup=builder.as_markup())


def is_admin(data: Dict, widget: Whenable, manager: DialogManager):
    user_id = data.get('user_id')
    admins = data.get('admins')
    return user_id in admins


async def show_data(callback: CallbackQuery, button: Button,
                    manager: DialogManager):
    if create_log_pass_txt():
        message = ''

        with open(FILE_LOG_PASS_PATH, 'r') as file:
            for line in file:
                message += line

        await callback.message.answer(message)
    else:
        await manager.switch_to(state=states.MainState.NODATA)


async def get_admins(callback: CallbackQuery, button: Button,
                     manager: DialogManager):
    admins = export_admins()
    message = ''
    for admin in admins:
        message += str(admin)
        message += '\n'

    await callback.message.answer('Все айдишники админов, записанные в базе:' + '\n' + f'{message}')


async def download_data(callback: CallbackQuery, button: Button,
                        manager: DialogManager):
    if create_log_pass_txt():
        await callback.message.answer_document(FILE_LOG_PASS)
    else:
        await manager.switch_to(state=states.MainState.NODATA)


main_dialog = Dialog(
    Window(
        Const("""
test"""),
        Start(
            text=Const("test"),
            id='choise',
            state=states.ChoiseState.CHOISE,
        ),
        Start(
            text=Const("test"),
            id='reviews',
            state=states.MainState.REVIEWS,
        ),
        Start(
            text=Const('Admin_mode'),
            id='admin',
            when=is_admin,
            state=states.MainState.ADMIN
        ),
        Cancel(Format('Выйти'), id='Exit', on_click=exit_dialog),
        state=states.MainState.MAIN,
    ),
    Window(
        Const('Сколько отобразить отзывов?'),

        Group(
            Row(
                Button(
                    Const("Последние 5"),
                    id="five_reviews",  # id is used to detect which button is clicked
                    on_click=get_five_reviews
                ),
                Button(
                    Const("Все"),
                    id="all_reviews",  # id is used to detect which button is clicked
                    on_click=get_all_reviews,
                ),
            ),
            Button(
                Const("test"),
                id="test",  # id is used to detect which button is clicked
                on_click=test
            ),
            SwitchTo(
                Const('Назад'),
                id='InStart',
                state=states.MainState.MAIN
            ),
        ),
        state=states.MainState.REVIEWS,
    ),

    Window(
        Const('Вы перешли в Админ-мод!'),
        Group(
            Row(
                Button(
                    Const('Выгрузить данные'),
                    id='download',
                    on_click=download_data,
                ),
                Button(
                    Const('Показать данные'),
                    id='show',
                    on_click=show_data,
                ),
            ),
            Button(
                Const('Все админы'),
                id='admins',
                on_click=get_admins,
            ),
            Back(
                Const('Exit'),
                id='back',
            ),
        ),
        state=states.MainState.ADMIN,
    ),

    Window(
        Const('Данных в базе нет'),
        SwitchTo(
            Const('Вернуться в админ-мод'),
            id='back_admin_mode',
            state=states.MainState.ADMIN
        ),
        SwitchTo(
            Const('Exit'),
            id='exit_admin_mode',
            state=states.MainState.MAIN
        ),
        state=states.MainState.NODATA
    ),

    Window(
        Const("Вы авторизуютесь второй раз, пройдите регистрацию заново..."),
        Const("Выберите площадку"),
        Start(
            text=Const("test"),
            id='test',
            state=states.ChoiseState.CHOISE,
        ),
        state=states.MainState.ERRORMAIN,
    ),

    launch_mode=LaunchMode.ROOT,
    getter=dialog_get_data
)
