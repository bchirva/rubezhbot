from vkbottle import API, BuiltinStateDispenser
from vkbottle.bot import BotLabeler

from ..config import VK_BOT_KEY, VK_GROUP_KEY

bot_api = API(VK_BOT_KEY)
group_api = API(VK_GROUP_KEY)

bot_labeler = BotLabeler()
bot_state = BuiltinStateDispenser()
group_labeler = BotLabeler()
