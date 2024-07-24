import os
import sys

try:  # На случай если при развёртывании кто-то забыл зависимости подтянуть
    from dotenv import load_dotenv
    import inspect
    import asyncio
    from aiogram.client.bot import DefaultBotProperties
    from aiogram import Bot, Dispatcher
    from aiogram.enums.parse_mode import ParseMode
    from aiogram.fsm.storage.memory import MemoryStorage
    from loguru import logger
except Exception:
    os.system('python -m pip install -r requirements.txt')
    from dotenv import load_dotenv
    import inspect
    import asyncio
    from aiogram import Bot, Dispatcher
    from aiogram.client.bot import DefaultBotProperties
    from aiogram.enums.parse_mode import ParseMode
    from aiogram.fsm.storage.memory import MemoryStorage
    from loguru import logger

from aio.handlers import router

load_dotenv()  # Подгружаем переменные окружения (для чувствительных данных)


# Эта функция гарантирует что рабочей директорией скрипта будет именно директория со скриптом и не придётся делать cd перед запуском
def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False):  # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)


os.chdir(get_script_dir())


async def main():
    bot = Bot(token=os.environ.get("BOT_TOKEN"),  default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
