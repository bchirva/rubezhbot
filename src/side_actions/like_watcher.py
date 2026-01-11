from loguru import logger
from vkbottle import GroupEventType, GroupTypes

from ..app import bot_api, group_api, route
from ..config import VK_GROUP_ID, VK_LIKES_REPORT_CHAT_ID


@route.raw_event(GroupEventType.LIKE_ADD, dataclass=GroupTypes.LikeAdd)
async def likes_report(event: GroupTypes.LikeAdd):
    if event.object.object_type != "post":
        return

    try:
        owner_id = event.object.object_owner_id
        if owner_id != -VK_GROUP_ID:
            return

        post_link = f"https://vk.com/wall{owner_id}_{event.object.object_id}"
        user_info = await group_api.users.get(user_ids=[event.object.liker_id])
        if not user_info:
            return

        user = user_info[0]
        user_name = f"{user.first_name} {user.last_name}"
        user_link = f"id{event.object.liker_id}"

        message = f"@{user_link} ({user_name}) лайкнул пост: {post_link}"
        logger.debug(message)

        await bot_api.messages.send(
            peer_id=VK_LIKES_REPORT_CHAT_ID, message=message, random_id=0
        )

    except Exception as error:
        logger.error("Ошибка при обработке реакта на пост на стене группы: {}", error)
