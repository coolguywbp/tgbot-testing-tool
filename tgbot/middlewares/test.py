from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from tgbot.services.test import Test


class TestMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, client):
        super().__init__()
        self.client = client
    async def pre_process(self, obj, data, *args):
        # Достаём имя выбранного бота, сохраненное в репозитории
        repo = data["repo"]
        try:
            user_id = obj.chat.id
        except AttributeError:
            user_id = obj.message.chat.id
        bot_name = await repo.get_bot_name(user_id)
        # Создаём объект с контроллером под этого бота
        # Также передаём bot, для realtime логирования
        data["test"] = Test(self.client, self.manager.bot, user_id, bot_name)

    async def post_process(self, obj, data, *args):
        del data["test"]
