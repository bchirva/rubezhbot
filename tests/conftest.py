import sys
from types import ModuleType, SimpleNamespace
from unittest.mock import AsyncMock


class TestRoute:
    def chat_message(self, **_kwargs):
        def decorator(handler):
            return handler

        return decorator


app_module = ModuleType("src.app")
app_module.route = TestRoute()
sys.modules["src.app"] = app_module

bot_module = ModuleType("vkbottle.bot")
bot_module.Message = object
vkbottle_module = ModuleType("vkbottle")
vkbottle_module.bot = bot_module
sys.modules["vkbottle"] = vkbottle_module
sys.modules["vkbottle.bot"] = bot_module


def make_message(text: str) -> SimpleNamespace:
    return SimpleNamespace(text=text, answer=AsyncMock())
