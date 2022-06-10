from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.models.role import UserRole
from tgbot.services.repository import Repo
from tgbot.services.test import Test

from tgbot.handlers.messages import messages

async def admin_start(m: Message, repo: Repo, test: Test):
    await repo.add_user(m.from_user.id)
    await m.answer(messages['start_message'])

async def show_users(m: Message, repo: Repo):
    list = await repo.list_users()
    await m.answer(list)

def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], role=UserRole.ADMIN)
    dp.register_message_handler(show_users, commands=["users"], role=UserRole.ADMIN)
    # # or you can pass multiple roles:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", role=[UserRole.ADMIN])
    # # or use another filter:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
