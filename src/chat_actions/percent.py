import random
import re

from vkbottle.bot import Message

from ..app import route

PERCENT_REGEXP = re.compile("/(?P<percent>[0-9]*)%$")


@route.chat_message(regexp=PERCENT_REGEXP)
async def check_percent(message: Message):
    match = re.match(PERCENT_REGEXP, message.text)
    if not match:
        return

    rand = random.randint(0, 100)
    percent = match.group("percent")

    result: str = "💯 Проверка вероятности: "
    if percent is None or percent == "":
        result += f"{rand}%"
    else:
        percent = int(percent)
        if percent > 100 or percent < 0:
            return
        result += f"{'УСПЕХ' if rand <= percent else 'ПРОВАЛ'} ({rand})"

    await message.answer(result)
