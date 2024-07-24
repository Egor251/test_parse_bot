import sys
import os
import inspect
import asyncio


def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False):  # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)

os.chdir(get_script_dir())

try:  # На случай если при развёртывании кто-то забыл зависимости подтянуть
    from loguru import logger
except Exception:
    os.system('python -m pip install -r requirements.txt')
    from loguru import logger

import aio.main_bot


if __name__ == '__main__':

    os.chdir(get_script_dir())
    logger.add('main_log.log', level='DEBUG', format="{time} {level} {message}", rotation="10 MB")  # Логгирование
    asyncio.run(aio.main_bot.main())
