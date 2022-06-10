from typing import List


class Repo:
    """Db abstraction layer"""

    def __init__(self, conn):
        self.conn = conn

    # users
    async def add_user(self, user_id, bot_name="@ruricbot") -> None:
        """Store user in DB, ignore duplicates"""
        await self.conn.execute(
            "insert or ignore into users values(:user_id, :bot_name)",
            {"user_id": user_id, "bot_name": bot_name}
        )
        await self.conn.commit()
        return

    async def list_users(self):
        """List all users"""
        cursor = await self.conn.execute("select * from users;")
        result = await cursor.fetchall()
        await cursor.close()
        return result

    async def get_bot_name(self, user_id):
        """List all users"""
        cursor = await self.conn.execute("select chosen_bot from users where user_id = :user_id;", {'user_id': user_id})
        result = await cursor.fetchone()
        return result[0]

    async def create_test(self, name, bot_name):
        """Create test in DB, ignore duplicates"""
        await self.conn.execute("insert or ignore into tests values(:name, :bot_name, NULL);", {'name': name, 'bot_name': bot_name})
        await self.conn.commit()
        return

    async def get_tests(self, bot_name):
        """List tests for selected bot"""
        cursor = await self.conn.execute("select * from tests where bot_name = :bot_name;", {'bot_name': bot_name})
        rows = await cursor.fetchall()
        await cursor.close()
        return rows

    async def get_test(self, name):
        """Get selected test"""
        cursor = await self.conn.execute("select * from tests where name = :name;", {'name': name})
        result = await cursor.fetchone()
        await cursor.close()
        # queries = [f'{i+1}) {query}' for i, query in enumerate(queries_string.split('\n'))]
        # return bot_name, '\n'.join(queries)
        return tuple(result)
