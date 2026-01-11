from vkbottle import Bot
from vkbottle.bot import run_multibot

# pylint: disable=unused-import
from . import side_actions
from .app import bot_api, group_api, route, state
from .utils import configure_log

configure_log()
bot = Bot(labeler=route, state_dispenser=state)
run_multibot(bot, [bot_api, group_api])
