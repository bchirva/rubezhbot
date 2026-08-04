import random
import re

from vkbottle.bot import Message

from ..app import route

DIE_REGEXP = re.compile("/(?P<count>[0-9]?)[dDkKдДкК](?P<edges>[0-9]+)?(?P<sign>[+-])?(?P<mod>[0-9]+)?$")


@route.chat_message(regexp=DIE_REGEXP)
async def roll_die(message: Message):
    match = re.match(DIE_REGEXP, message.text)
    if not match:
        return

    count = int(match.group("count") or 1)
    edges = int(match.group("edges") or 20)
    sign = match.group("sign")
    mod_raw = match.group("mod")
    mod = 0

    if sign and mod_raw is None:
        sign = None


    if sign and mod_raw is not None:
        mod = int(mod_raw) if sign == '+' else -int(mod_raw)

    if count <= 0 or edges <= 0:
        return

    result: str = f"🎲 Бросок кост{'ей' if count > 1 else 'и'} d{edges}: "

    for _ in range(count):
        if (sign and mod_raw):
            rand_die = random.randint(1, edges)
            result += f"\n {rand_die + mod} ({rand_die}{sign}{mod_raw})"
        else:
            result += f"\n {random.randint(1, edges)} "

    await message.answer(result)
