import asyncio
import logging
import aiosqlite

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage

from pyrogram import Client

from tgbot.config import load_config
from tgbot.filters.role import RoleFilter, AdminFilter

from tgbot.handlers.admin import register_admin
from tgbot.handlers.user import register_user

from tgbot.middlewares.db import DbMiddleware
from tgbot.middlewares.role import RoleMiddleware
from tgbot.middlewares.test import TestMiddleware

logger = logging.getLogger(__name__)

# Sqlite3
async def create_pool(path):
    return await aiosqlite.connect(path)

# Pyrogram Client
async def create_client(session_string, api_id, api_hash, phone_number):
    client = Client(
        session_string,
        api_id=api_id,
        api_hash=api_hash,
        phone_number=phone_number
    )
    await client.start()
    # print(await client.export_session_string())
    return client

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    config = load_config("bot.ini")

    if config.tg_bot.use_redis:
        storage = RedisStorage()
    else:
        storage = MemoryStorage()

    pool = await create_pool('sqlite3.db')

    bot = Bot(token=config.tg_bot.token, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot, storage=storage)

    client = await create_client(
        config.pyrogram_client.session_string,
        config.pyrogram_client.api_id,
        config.pyrogram_client.api_hash,
        config.pyrogram_client.phone_number
    )

    dp.middleware.setup(DbMiddleware(pool))
    dp.middleware.setup(RoleMiddleware(config.tg_bot.admin_id))
    dp.middleware.setup(TestMiddleware(client))

    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)

    register_admin(dp)
    register_user(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()

        await pool.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
