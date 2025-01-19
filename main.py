from aiogram import Bot,Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode


from handlers.user import user
from database.engine import create_db, drop_db, session_maker
from middlewares.db import DataBaseSession

from environs import Env
import asyncio

async def main():
    env = Env()
    env.read_env()
    
    
    bot=Bot(token=env('TOKEN'),default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    
    
    dp.include_routers(user)
    
    async def on_startup(bot):
        run_param = False
        if run_param:
            await drop_db()
        await create_db()
    async def on_shutdown(bot):
        print('бот лег')
    
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    
    await bot.delete_webhook(drop_pending_updates=True)
    
    await dp.start_polling(bot)

asyncio.run(main())