from typing import List

class Test:
    """Tester abstraction layer"""

    def __init__(self, controller):
        self.controller = controller

    # test commands
    async def test_start(self) -> None:

        async with self.controller.collect(count=1) as response:
            await self.controller.send_command("start")

        assert response.num_messages == 1  # Three messages received, bundled under a `Response` object
        
    def run_query(self, query):
        splitted_query = tuple(query.split('->'))
        if len(splitted_query) != 2:
            return('Wrong query.')
        input, output = splitted_query
        return input
