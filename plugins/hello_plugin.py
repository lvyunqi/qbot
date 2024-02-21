# plugins/hello_plugin.py
from botpy.ext.command_util import Commands
from botpy.message import Message
from botpy import BotAPI

@Commands("你好", "hello")
async def hello(api: BotAPI, message: Message, params=None):
    await api.post_message(channel_id=message.channel_id, content='Hello,World!', msg_id=message.id)
    return True

@Commands("晚安")
async def good_night(api: BotAPI, message: Message, params=None):
    await message.reply(content=params)
    return True
