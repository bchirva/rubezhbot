import asyncio

import pytest

from src.chat_actions import dice

from conftest import make_message


@pytest.mark.parametrize(
    ("command", "count", "edges", "sign", "mod", "comment"),
    [
        ("/d", "", None, None, None, ""),
        ("/2d12", "2", "12", None, None, ""),
        ("/d20+5", "", "20", "+", "5", ""),
        ("/3к8-2 проверка ловкости", "3", "8", "-", "2", " проверка ловкости"),
    ],
)
def test_die_regexp_parses_command(command, count, edges, sign, mod, comment):
    match = dice.DIE_REGEXP.fullmatch(command)

    assert match is not None
    assert match.groupdict() == {
        "count": count,
        "edges": edges,
        "sign": sign,
        "mod": mod,
        "comment": comment,
    }


@pytest.mark.parametrize("command", ["d6", "/d0", "/0d6"])
def test_roll_die_ignores_invalid_commands(command):
    message = make_message(command)

    asyncio.run(dice.roll_die(message))

    message.answer.assert_not_awaited()


def test_roll_die_outputs_regular_roll(monkeypatch):
    monkeypatch.setattr(dice.random, "randint", lambda _start, _end: 4)
    message = make_message("/d6")

    asyncio.run(dice.roll_die(message))

    message.answer.assert_awaited_once_with("🎲 Бросок кости d6: \n 4 ")


def test_roll_die_outputs_critical_results(monkeypatch):
    rolls = iter([1, 6, 3])
    monkeypatch.setattr(dice.random, "randint", lambda _start, _end: next(rolls))
    message = make_message("/3d6")

    asyncio.run(dice.roll_die(message))

    message.answer.assert_awaited_once_with(
        "🎲 Бросок костей d6: \n 💀 1 \n 💥 6 \n 3 "
    )


def test_roll_die_applies_modifier_and_comment(monkeypatch):
    monkeypatch.setattr(dice.random, "randint", lambda _start, _end: 20)
    message = make_message("/d20+3 атака")

    asyncio.run(dice.roll_die(message))

    message.answer.assert_awaited_once_with(
        "🎲 Бросок кости d20 (атака): \n 💥 23 (20+3)"
    )
