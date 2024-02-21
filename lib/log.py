from botpy import BotAPI
from botpy import logging
from botpy.message import Message

_log = logging.get_logger()

async def msg_log(api: BotAPI, message: Message):
    guild_info = await api.get_guild(guild_id=message.guild_id)
    channel_info = await api.get_channel(channel_id=message.channel_id)
    if message.content is None:
        string = '['
        for attachment in message.attachments:
            string += f"({attachment.content_type}: {attachment.url})\n"
        string = string[:-1]
        string += ']'
        _log.info(f"[{guild_info['name']}]({channel_info['name']}): {message.author.username} -> msg: {string}")
        return False
    else:
        _log.info(f"[{guild_info['name']}]({channel_info['name']}): {message.author.username} -> msg: {message.content}")
    return False