import os

from botpy import BotAPI
from botpy import logging
from botpy.ext.cog_yaml import read

from botpy.logging import DEFAULT_FILE_HANDLER

_log = logging.get_logger()

class PluginManager:
    _plugins = []

    def init():
        PluginManager.init_dir()
        PluginManager.log_config()

    def init_dir():
        if not os.path.exists(os.path.join(os.getcwd(), "temp", "log")):
            os.makedirs(os.path.join(os.getcwd(), "temp", "log"))

    def config():
        return read(os.path.join(os.getcwd(), "config.yaml"))
    
    def log_config():
        DEFAULT_FILE_HANDLER["filename"] = os.path.join(os.getcwd() + '/temp', "log", "%(name)s.log")

    @classmethod
    def register(cls, plugin):
        cls._plugins.append(plugin)

    @classmethod
    async def process_event(cls, api: BotAPI, message):
        _log.info(f"message: {message.content}")
        for plugin in cls._plugins:
            if await plugin(api=api, message=message):
                return True
        return False