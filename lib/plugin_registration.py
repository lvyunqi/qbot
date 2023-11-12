import os
import importlib
import inspect
from botpy import logging
from lib.plugin_manager import PluginManager

_log = logging.get_logger()

class PluginRegistration:

    def __init__(self):
        self.loaded_modules = set()

    def get_functions(self, module: object) -> list:
        '''
        获取模块的可用函数列表
        '''
        functions = inspect.getmembers(module, inspect.isfunction)
        return [name for name, _ in functions]

    def load_plugin_module(self, plugin_dir, plugin_name):
        key = f"{plugin_dir}.{plugin_name}"

        try:
            module = importlib.import_module(key)

            # 如果已经加载过，尝试重新加载
            if key in self.loaded_modules:
                module = importlib.reload(module)
            else:
                self.loaded_modules.add(key)

            return module
        except Exception as e:
            _log.error(f"加载插件[{plugin_name}]失败，原因：{e}")
            return None

    def register_plugins(self, config):
        plugin_dirs = config["plugin_dir"]
        plugins = config["plugins"]

        for plugin_dir in plugin_dirs:
            try:
                for plugin_file in os.listdir(plugin_dir):
                    if plugin_file.endswith(".py") and plugin_file != "__init__.py":
                        plugin_name = os.path.splitext(plugin_file)[0]
                        if plugin_name not in plugins:
                            continue

                        module = self.load_plugin_module(plugin_dir, plugin_name)
                        if module:
                            functions = self.get_functions(module)
                            for func_name in functions:
                                func = getattr(module, func_name)
                                if callable(func):
                                    PluginManager.register(func)
                            _log.info(f"插件[{plugin_name}]加载成功")
            except Exception as e:
                _log.error(f"加载插件集[{plugin_dir}]失败，原因：{e}")
                continue
            _log.info(f"插件集[{plugin_dir}]加载成功")
        _log.info("插件加载完毕")
