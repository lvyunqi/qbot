<div align="center">

_✨ 基于 [腾讯机器人开放平台官方SDK](https://bot.q.qq.com/wiki/develop/api/) 实现的轻量便捷插件化机器人框架 ✨_

_✨ 为开发者提供一个易使用、开发效率高的开发框架 ✨_


</div>



# 安装教程

## 环境要求

- Python 3.8+

## 环境配置

```bash
pip install -r requirements.txt   # 安装依赖的pip包
```

## 配置文件

根目录下的`config.yaml`为基础插件配置文件，可在此配置频道机器人的基础信息

## 开发流程

默认插件目录为`plugins`，可在`plugins`目录下创建一个插件文件或者插件文件夹，例如`hello_plugin.py`，在`hello_plugin.py`中编写插件代码，例如：

```python
# plugins/hello_plugin.py
from botpy.ext.command_util import Commands
from botpy.message import Message
from botpy import BotAPI

@Commands(name=("你好", "hello"))
async def hello(api: BotAPI, message: Message, params=None):
    await api.post_message(channel_id=message.channel_id, content="params", msg_id=message.id)
    await message.reply(content=params)
    return True

@Commands("晚安")
async def good_night(api: BotAPI, message: Message, params=None):
    await message.reply(content=params)
    return True
```

请根据官方(QQ频道机器人SDK)[QQ频道机器人SDK](https://bot.q.qq.com/wiki/develop/pythonsdk/)文档编写插件代码


## 运行机器人

```bash 
python main.py
```     