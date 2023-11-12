import os
import inspect
import importlib

from botpy import logging
from lib.plugin_manager import PluginManager

_log = logging.get_logger()

class PluginRegistration:

    def get_members(self, module: object) -> list:
        '''
        获取模块的可用成员列表
        '''
        members_list = []
        members = inspect.getmembers(module)
        for name, member in members:
            if inspect.isfunction(member):
                members_list.append(name)
        return members_list
    
    def get_not_members(self, module: object, depth=1, max_depth=3) -> list:
        '''
        获取模块的非成员列表
        '''
        members_list = []
        if depth <= max_depth:
            for member_name in dir(module):
                if member_name[0] != "_":
                    members_list.append(member_name)
                    # 继续调用自身，查找更深层次的成员
                    members_list.extend(self.get_not_members(getattr(module, member_name), depth + 1, max_depth))
        return members_list

    def register(self,config: dict):
        plugin_dirs = config["plugin_dir"]
        plugins = config["plugins"]
        for plugin_dir in plugin_dirs:
            try:
                for plugin_file in os.listdir(plugin_dir):
                    if plugin_file.endswith(".py") and plugin_file != "__init__.py":
                        plugin_name = os.path.splitext(plugin_file)[0]
                        if plugin_name not in plugins:
                            continue
                        module = importlib.import_module(f"{plugin_dir}.{plugin_name}")
                        for obj in dir(module):
                            if obj in self.get_members(module):
                                attr = getattr(module, obj)
                                if callable(attr):
                                    PluginManager.register(attr)
                            else:
                                continue
            except Exception as e:
                _log.error(f"加载插件[{plugin_dir}]失败，原因：{e}")
                continue
            _log.info(f"插件[{plugin_dir}]加载成功")
        _log.info("插件加载完毕")
            
                        