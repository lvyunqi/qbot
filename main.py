# -*- coding: utf-8 -*-
import botpy

from lib.plugin_manager import PluginManager
from lib.plugin_registration import PluginRegistration

app = PluginManager()
app.init()

config = app.config()
PluginRegistration().register_plugins(config)

class MyClient(botpy.Client):
    async def on_message_create(self, message):
        await app.process_event(api=self.api, message=message)


if __name__ == "__main__":
    intents = botpy.Intents(guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=config["appid"], token=config["token"])
