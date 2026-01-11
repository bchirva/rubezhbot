from typing import Dict

from vkbottle import BaseStateGroup, Keyboard, Text
from vkbottle.bot import Message

from ..app import route, state
from ..domain import Character, Fraction, FractionsRegistry, Membership, Rank
from ..utils import payload_value

sign_ups: Dict[int, Character] = {}

CONFIRM_CMD = {"cmd": "confirm"}
REJECT_CMD = {"cmd": "reject"}
CONFIRM_KEYBOARD = (
    Keyboard(one_time=True)
    .add(Text("Да", payload={"cmd": "confirm"}))
    .add(Text("Нет", payload={"cmd": "reject"}))
    .get_json()
)
FRACTION_IDX = "fraction_idx"


async def reset_sing_up(peer_id: int):
    await state.delete(peer_id)


def get_fraction_idx(message: Message):
    return (
        message.state_peer.payload.get(FRACTION_IDX, 1) if message.state_peer else None
    ) or 1


class SignUpState(BaseStateGroup):  # pylint: disable=invalid-enum-extension
    INIT = "init"
    NAME = "name"
    NAME_CONFIRM = "name-confirm"
    AGE = "age"
    AGE_CONFIRM = "age-confirm"
    FRACTION = "faction"
    FRACTION_CONFIRM = "faction-confirm"
    RANK = "rank"
    RANK_CONFIRM = "rank-confirm"
    ROLE = "role"
    ROLE_CONFIRM = "role-confirm"
    FINAL_CHECK = "final-check"
    NEXT_FRACTION = "next-fraction"


@route.private_message(state=None, payload={"cmd": "sign-up"})
async def sing_up_init(message: Message):
    await state.set(message.peer_id, SignUpState.INIT)
    await message.answer("Начать регистрацию?", keyboard=CONFIRM_KEYBOARD)


@route.private_message(state=SignUpState.INIT, payload=REJECT_CMD)
async def sing_up_cancel(message: Message):
    await reset_sing_up(message.peer_id)


@route.private_message(state=SignUpState.INIT, payload=CONFIRM_CMD)
@route.private_message(state=SignUpState.NAME_CONFIRM, payload=REJECT_CMD)
async def sign_up_name(message: Message):
    await state.set(message.peer_id, SignUpState.NAME)
    await message.answer("1. Введите имя персонажа")


@route.private_message(state=SignUpState.NAME)
async def sign_up_name_confirm(message: Message):
    await state.set(message.peer_id, SignUpState.NAME_CONFIRM)
    sign_ups[message.peer_id].name = message.text
    await message.answer(
        f"Имя персонажа: {message.text}, верно?", keyboard=CONFIRM_KEYBOARD
    )


@route.private_message(state=SignUpState.NAME_CONFIRM, payload=CONFIRM_CMD)
@route.private_message(state=SignUpState.AGE_CONFIRM, payload=REJECT_CMD)
async def sign_up_age(message: Message):
    await state.set(message.peer_id, SignUpState.AGE)
    await message.answer("2. Введите возраст персонажа")


@route.private_message(state=SignUpState.AGE)
async def sign_up_age_confirm(message: Message):
    await state.set(message.peer_id, SignUpState.AGE_CONFIRM)
    sign_ups[message.peer_id].age = int(message.text)
    await message.answer(
        f"Возраст персонажа: {message.text}, верно?", keyboard=CONFIRM_KEYBOARD
    )


@route.private_message(state=SignUpState.AGE_CONFIRM, payload=CONFIRM_CMD)
@route.private_message(state=SignUpState.FRACTION_CONFIRM, payload=REJECT_CMD)
@route.private_message(state=SignUpState.NEXT_FRACTION, payload=CONFIRM_CMD)
async def sign_up_fraction(message: Message):
    fraction_idx = get_fraction_idx(message)
    await state.set(message.peer_id, SignUpState.FRACTION, fraction_idx=fraction_idx)

    fraction_keyboard = Keyboard(one_time=True)
    for fraction in FractionsRegistry().get_all():
        fraction_keyboard.add(
            Text(
                f"{fraction.logo} {fraction.name}", payload={"fraction_id": fraction.id}
            )
        )

    await message.answer("3. Выберите фракцию", keyboard=fraction_keyboard.get_json())


@route.private_message(state=SignUpState.FRACTION)
async def sign_up_fraction_confirm(message: Message):
    fraction_idx = get_fraction_idx(message)
    await state.set(
        message.peer_id, SignUpState.FRACTION_CONFIRM, fraction_idx=fraction_idx
    )

    fraction_id = payload_value(message.payload, "fraction_id")
    if fraction_id is None:
        await reset_sing_up(message.peer_id)
        return

    fraction = FractionsRegistry().get_by_id(fraction_id=fraction_id)
    if fraction is None:
        await reset_sing_up(message.peer_id)
        return

    if len(sign_ups[message.peer_id].factions) < fraction_idx:
        sign_ups[message.peer_id].factions.append(Membership())

    sign_ups[message.peer_id].factions[fraction_idx - 1] = Membership(
        fraction=fraction, rank=Rank(), comment=""
    )

    await message.answer(
        f"Выбраная фракция {fraction.logo} {fraction.name}, верно?",
        keyboard=CONFIRM_KEYBOARD,
    )


@route.private_message(state=SignUpState.FRACTION_CONFIRM, payload=CONFIRM_CMD)
@route.private_message(state=SignUpState.RANK_CONFIRM, payload=REJECT_CMD)
async def sign_up_rank(message: Message):
    fraction_idx = get_fraction_idx(message)
    await state.set(message.peer_id, SignUpState.RANK, fraction_idx=fraction_idx)

    rank_keyboard = Keyboard(one_time=True)
    for rank in FractionsRegistry().get_fraction_ranks(1):
        rank_keyboard.add(
            Text(f"{rank.level}. {rank.name}", payload={"rank_level": rank.level})
        )

    await message.answer(
        "3. Выберите ранг во фракции", keyboard=rank_keyboard.get_json()
    )


@route.private_message(state=SignUpState.RANK)
async def sign_up_rank_confirm(message: Message):
    fraction_idx = get_fraction_idx(message)
    await state.set(
        message.peer_id, SignUpState.RANK_CONFIRM, fraction_idx=fraction_idx
    )
    await state.set(
        message.peer_id, SignUpState.RANK_CONFIRM, fraction_idx=fraction_idx
    )

    fraction_id = sign_ups[message.peer_id].factions[fraction_idx - 1].fraction.id
    rank_level = payload_value(message.payload, "rank_level")
    if rank_level is None:
        await reset_sing_up(message.peer_id)
        return

    rank = FractionsRegistry().get_fraction_rank_level(
        fraction_id=fraction_id, rank_level=rank_level
    )
    if rank is None:
        await reset_sing_up(message.peer_id)
        return

    sign_ups[message.peer_id].factions[fraction_idx - 1].rank = rank

    await message.answer(
        f"Выбраный ранг во фракции - {rank.name} ({rank.level}), верно?",
        keyboard=CONFIRM_KEYBOARD,
    )


@route.private_message(state=SignUpState.RANK_CONFIRM, payload=CONFIRM_CMD)
@route.private_message(state=SignUpState.ROLE_CONFIRM, payload=REJECT_CMD)
async def sign_up_role(message: Message):
    fraction_idx = get_fraction_idx(message)
    await state.set(message.peer_id, SignUpState.ROLE, fraction_idx=fraction_idx)
    await message.answer("4. Выберите роль во фракции")


@route.private_message(state=SignUpState.ROLE)
async def sign_up_role_confirm(message: Message):
    fraction_idx = get_fraction_idx(message)
    await state.set(
        message.peer_id, SignUpState.ROLE_CONFIRM, fraction_idx=fraction_idx
    )
    sign_ups[message.peer_id].factions[fraction_idx - 1].comment = message.text
    await message.answer(
        f"Роль персонажа во фракции: {message.text}, верно?", keyboard=CONFIRM_KEYBOARD
    )


@route.private_message(state=SignUpState.ROLE_CONFIRM, payload=CONFIRM_CMD)
async def sign_up_next_fraction(message: Message):
    fraction_idx = get_fraction_idx(message)

    # await state.set(
    #     message.peer_id, SignUpState.NEXT_FRACTION, fraction_idx=fraction_idx
    # )
    # await message.answer(
    #     "Персонаж зарегистрирован во фракции, добавить стороннюю фракцию?",
    #     keyboard=CONFIRM_KEYBOARD,
    # )
    #
    # await state.delete(message.peer_id)
    # await message.answer(f"Регистрация завершена! ID персонажа {1}")
