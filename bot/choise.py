from aiogram.types import CallbackQuery, FSInputFile
from aiogram_dialog import Dialog, LaunchMode, Window, DialogManager
from aiogram_dialog.widgets.kbd import Start, Row, Button
from aiogram_dialog.widgets.text import Const

from . import states

async def one(callback: CallbackQuery, button: Button,
                    manager: DialogManager):
    await callback.message.answer_photo(test)

async def two(callback: CallbackQuery, button: Button,
                    manager: DialogManager):
    await callback.message.answer_photo(test)

choise_dialog = Dialog(
    Window(
        Const("test"),
        Row(
            Start(
                text=Const("test"),
                id="test",
                state=states.test.MAIN,
                on_click=test
            ),
            Start(
                text=Const("test"),
                id="test",
                state=states.test.MAIN,
                on_click=1
            ),
        ),
        state=states.ChoiseState.CHOISE,
    ),
    launch_mode=LaunchMode.ROOT,
)
