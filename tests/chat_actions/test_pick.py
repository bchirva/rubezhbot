import asyncio

import pytest

from src.chat_actions.pick import PICK_REGEXP, pick, random

from conftest import make_message


@pytest.mark.parametrize(
    ("command", "variants"),
    [
        ("/? орёл, решка", "орёл, решка"),
        ("/? красный дракон,синий маг", "красный дракон,синий маг"),
    ],
)
def test_pick_regexp_parses_command(command, variants):
    match = PICK_REGEXP.fullmatch(command)

    assert match is not None
    assert match.group("variants") == variants


@pytest.mark.parametrize(
    "command", ["? орёл, решка", "/?", "/? один", "/? один,", "/? один,, два"]
)
def test_pick_ignores_invalid_commands(command):
    message = make_message(command)

    asyncio.run(pick(message))

    message.answer.assert_not_awaited()


def test_pick_outputs_selected_trimmed_variant(monkeypatch):
    def choose(variants):
        assert variants == ["красный дракон", "синий маг"]
        return variants[1]

    monkeypatch.setattr(random, "choice", choose)
    message = make_message("/?  красный дракон, синий маг  ")

    asyncio.run(pick(message))

    message.answer.assert_awaited_once_with("❓выбор: синий маг")
