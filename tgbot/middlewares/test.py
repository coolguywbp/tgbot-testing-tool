from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from tgintegration import BotController
from tgbot.services.test import Test


class TestMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.peer = "@ruricbot"
        self.controller = BotController(
            peer=self.peer,      # The bot under test is https://t.me/BotListBot 🤖
            client=self.client,           # This assumes you already have a Pyrogram user client available
            max_wait=8,              # Maximum timeout for responses (optional)
            wait_consecutive=2,      # Minimum time to wait for more/consecutive messages (optional)
            raise_no_response=True,  # Raise `InvalidResponseError` when no response is received (defaults to True)
            global_action_delay=2.5  # Choosing a rather high delay so we can observe what's happening (optional)
        )

    async def pre_process(self, obj, data, *args):
        data["test"] = Test(self.controller)

    async def post_process(self, obj, data, *args):
        del data["test"]
