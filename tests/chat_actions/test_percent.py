import asyncio

import pytest

from src.chat_actions import percent

from conftest import make_message


@pytest.mark.parametrize(
    ("command", "value", "comment"),
    [
        ("/%", "", ""),
        ("/0%", "0", ""),
        ("/100%", "100", ""),
        ("/70% проверка удачи", "70", " проверка удачи"),
    ],
)
def test_percent_regexp_parses_command(command, value, comment):
    match = percent.PERCENT_REGEXP.fullmatch(command)

    assert match is not None
    assert match.group("percent") == value
    assert match.group("comment") == comment


@pytest.mark.parametrize("command", ["50%", "/50", "/-1%", "/101 %"])
def test_percent_regexp_rejects_invalid_syntax(command):
    assert percent.PERCENT_REGEXP.fullmatch(command) is None


def test_check_percent_outputs_random_percent_with_comment(monkeypatch):
    monkeypatch.setattr(percent.random, "randint", lambda _start, _end: 42)
    message = make_message("/% погода")

    asyncio.run(percent.check_percent(message))

    message.answer.assert_awaited_once_with("💯 Проверка вероятности (погода): 42%")


@pytest.mark.parametrize(
    ("command", "roll", "expected"),
    [
        ("/70%", 70, "💯 Проверка вероятности: 🎉 УСПЕХ (70)"),
        ("/70%", 71, "💯 Проверка вероятности: 🪊 ПРОВАЛ (71)"),
        ("/70% проверка", 70, "💯 Проверка вероятности (проверка): 🎉 УСПЕХ (70)"),
        ("/0%", 0, "💯 Проверка вероятности: 🎉 УСПЕХ (0)"),
        ("/100%", 100, "💯 Проверка вероятности: 🎉 УСПЕХ (100)"),
    ],
)
def test_check_percent_outputs_check_result(monkeypatch, command, roll, expected):
    monkeypatch.setattr(percent.random, "randint", lambda _start, _end: roll)
    message = make_message(command)

    asyncio.run(percent.check_percent(message))

    message.answer.assert_awaited_once_with(expected)


@pytest.mark.parametrize("command", ["/101%", "/999%", "/-1%"])
def test_check_percent_ignores_out_of_range_value(command):
    message = make_message(command)

    asyncio.run(percent.check_percent(message))

    message.answer.assert_not_awaited()
