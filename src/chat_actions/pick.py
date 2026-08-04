import random
import re

from vkbottle.bot import Message

from ..app import route

PICK_REGEXP = re.compile(r"/\?\s*(?P<variants>.+)$")


@route.chat_message(regexp=PICK_REGEXP)
async def pick(message: Message):
    match = re.match(PICK_REGEXP, message.text)
    if not match:
        return

    variants = [variant.strip() for variant in match.group("variants").split(",")]
    if len(variants) < 2 or not all(variants):
        return

    await message.answer(f"❓выбор: {random.choice(variants)}")
