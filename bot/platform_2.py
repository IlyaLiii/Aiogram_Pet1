import time
from random import randint

import validators
from aiogram.types import ContentType, Message

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const

from . import states


async def md5_input_2(message: Message, message_input: MessageInput,
                    manager: DialogManager):
    md5 = message.text
    user_id = message.from_user.id

    if validators.hashes.md5(md5):
        rand = randint(1, 2) ### rand = randint(1, 2)  rand = randint(5, 15)
        await message.answer(f'test')
        time.sleep(rand)
        middleware_data = manager.middleware_data
        await manager.start(state=states.test.MAIN, data={'md5': md5, 'middleware_data': middleware_data})

    else:
        await message.answer('Некорректный ввод MD5-ХЭША')
        await manager.switch_to(state=states.test.NOVALID)


platfrom_2 = Window(
    Const('''
test
'''),
    MessageInput(test, content_types=[ContentType.TEXT]),
    state=states.test.MAIN,
)

platfrom_2_error_md5 = Window(
    Const('Введите корректный MD5-ХЭШ: '),
    MessageInput(test, content_types=[ContentType.TEXT]),
    state=states.test.NOVALID,
)

platfrom_dialog_2 = Dialog(
    platfrom_2,
    platfrom_2_error_md5,
)
