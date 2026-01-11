import random
import re

from vkbottle.bot import Message

from ..app import route

DIE_REGEXP = re.compile("/(?P<count>[0-9]?)[dDkKдДкК](?P<edges>[0-9]+)$")


@route.chat_message(regexp=DIE_REGEXP)
async def roll_die(message: Message):
    match = re.match(DIE_REGEXP, message.text)
    if not match:
        return

    count = int(match.group("count") or 1)
    edges = int(match.group("edges"))

    if count < 0 or edges < 0:
        return

    result: str = f"🎲 Бросок кост{'ей' if count > 1 else 'и'} d{edges}: "

    for _ in range(count):
        result += f"{random.randint(1, edges)} "

    await message.answer(result)
