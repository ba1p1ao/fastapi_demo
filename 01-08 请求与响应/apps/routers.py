# routers.py
import importlib
from fastapi import APIRouter
from pathlib import Path

def auto_discover_routers(app_package: str = "apps"):
    """自动发现并加载所有路由"""
    routers = []
    apps_path = Path(__file__).parent / app_package
    print(apps_path)
    for app_dir in apps_path.iterdir():
        if app_dir.is_dir() and not app_dir.name.startswith('__'):
            try:
                module_name = f"{app_package}.{app_dir.name}"
                module = importlib.import_module(module_name)
                
                # 查找模块中的 APIRouter 实例
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, APIRouter):
                        routers.append(attr)
                        break
            except ImportError as e:
                print(f"Failed to import {app_dir.name}: {e}")
    
    return routers

# 使用
if __name__ == "__main__":
    routers = auto_discover_routers()