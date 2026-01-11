from vkbottle import Keyboard, Text
from vkbottle.bot import Message

from ..app import route

ROOT_KEYBOARD = (
    Keyboard(one_time=True)
    .add(Text("📝 Зарегистрироваться", payload={"cmd": "sign-up"}))
    .add(Text("💲 Банк", payload={"cmd": "bank"}))
)


@route.private_message(state=None, payload=None)
async def root_keyboard(message: Message):
    await message.answer(
        "Здравствуйте, чего желаете?", keyboard=ROOT_KEYBOARD.get_json()
    )
