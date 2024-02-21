import os
from botpy import BotAPI
from botpy.message import Message
from botpy.ext.cog_yaml import read
from botpy.logging import DEFAULT_FILE_HANDLER
from lib.log import msg_log

class PluginManager:
    _plugins = []

    def __init__(self, config_dir='', log_dir="temp/log"):
        self.config_dir = config_dir
        self.log_dir = log_dir

    def init(self):
        self.init_dir()
        self.log_config()

    def init_dir(self):
        log_dir_path = os.path.join(os.getcwd(), self.log_dir)
        if not os.path.exists(log_dir_path):
            os.makedirs(log_dir_path)

    def config(self):
        return read(os.path.join(os.getcwd(), self.config_dir, "config.yaml"))

    def log_config(self):
        DEFAULT_FILE_HANDLER["filename"] = os.path.join(os.getcwd(), self.log_dir, "%(name)s.log")

    @classmethod
    def register(cls, plugin):
        cls._plugins.append(plugin)

    @classmethod
    async def process_event(cls, api: BotAPI, message: Message):
        await msg_log(api=api, message=message)
        for plugin in cls._plugins:
            if await plugin(api=api, message=message):
                return True
        return False
