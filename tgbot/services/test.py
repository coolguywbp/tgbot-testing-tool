from typing import List

from tgintegration import BotController
from tgintegration.containers.responses import InvalidResponseError

class Test:
    """Tester abstraction layer"""

    def __init__(self, client, bot, user_id, peer):
        self.client = client
        self.bot = bot
        self.user_id = user_id
        self.peer = peer
        self.controller = BotController(
            peer=self.peer,
            client=self.client,
            max_wait=5,              # Maximum timeout for responses (optional)
            wait_consecutive=2,      # Minimum time to wait for more/consecutive messages (optional)
            raise_no_response=True,  # Raise `InvalidResponseError` when no response is received (defaults to True)
            global_action_delay=2.5  # Choosing a rather high delay so we can observe what's happening (optional)
        )
        self.actions = ('type', 'press')
        self.types = ('text', 'audio', 'voice', 'video')
        self.operators = ('has', 'has_inline', 'has_reply')
    # realtime logging
    async def log(self, event):
        return await self.bot.send_message(self.user_id, event)

    async def test_start(self) -> None:

        async with self.controller.collect(count=1) as response:
            await self.controller.send_command("start")

        assert response.num_messages == 1  # Three messages received, bundled under a `Response` object

    async def run_test(self, queries):
        await self.log('🛁 Удаляю историю')
        await self.controller.clear_chat()
        queries = queries.split('\n')
        passed_queries = []
        for query in queries:
            passed_queries.append(await self.run_query(query[:-2]))
        return passed_queries

    async def run_query(self, query, clear_chat = False):
        parsed_query = self._parse_query(query)
        if parsed_query[0] == 'error':
            await self.log(parsed_query[1])
            return False
        parsed_input, expected_types, expected_content = parsed_query[1]
        expected_num = len(expected_types)

        response = None
        await self.log(f'🤟 Начинаю проверку для {self.peer}:\n<code>{query}</code>')
        if clear_chat:
            await self.log('🛁 Удаляю историю')
            await self.controller.clear_chat()

        cursor_message = None
        # Вводим команду
        if parsed_input[0] == 'cmd':
            try:
                await self.log(f'✅ Отправляю команду /{parsed_input[1]}')
                await self.log(f'⏱ Ожидаю ответ...')
                async with self.controller.collect(count=expected_num) as res:
                    await self.controller.send_command(parsed_input[1])
                    response = res
            except InvalidResponseError:
                await self.log(f'❌ Получено ответов <b>{response.num_messages}</b>/<b>{expected_num}</b>')
                await self.log(f'❌ {self.peer} не удовлетворяет проверке:\n<code>{query}</code>')
                return False

        # Вводим текст
        elif parsed_input[0] == 'text':
            await self.log(f'✅ Отправляю текст "{parsed_input[1]}"')
            await self.log(f'⏱ Ожидаю ответ...')
            async with self.controller.collect(count=expected_num, raise_=False) as res:
                await self.client.send_message(self.controller.peer_id, parsed_input[1].replace("'", ''))
                response = res

        # Проверяем количество полученных сообщений

        try:
            assert response.num_messages == expected_num
        except AssertionError:
            await self.log(f'❌ Получено ответов <b>{response.num_messages}</b>/<b>{expected_num}</b>')
            await self.log(f'❌ {self.peer} не удовлетворяет проверке:\n<code>{query}</code>')
            return False

        await self.log(f'✅ Получено <b>{expected_num}</b>/<b>{response.num_messages}</b> ответов')

        # Проверяем типы сообщений
        for i, type in enumerate(expected_types):
            if type == 'text':
                try:
                    assert response.messages[i].text
                    await self.log(f'✅ {i+1} ответ является текстом')
                except AssertionError:
                    await self.log(f'❌ {i+1} ответ не является текстом')
                    await self.log(f'❌ {self.peer} не удовлетворяет проверке:\n<code>{query}</code>')
                    return False
            elif type == 'video':
                try:
                    assert response.messages[i].video
                    await self.log(f'✅ {i+1} ответ является видео')
                except AssertionError:
                    await self.log(f'❌ {i+1} ответ не является видео')
                    await self.log(f'❌ {self.peer} не удовлетворяет проверке:\n<code>{query}</code>')
                    return False
            elif type == 'audio':
                try:
                    assert response.messages[i].audio
                    await self.log(f'✅ {i+1} ответ является аудио')
                except AssertionError:
                    await self.log(f'❌ {i+1} ответ не является аудио')
                    await self.log(f'❌ {self.peer} не удовлетворяет проверке:\n<code>{query}</code>')
                    return False
            elif type == 'voice':
                try:
                    assert response.messages[i].voice
                    await self.log(f'✅ {i+1} ответ является голосовым')
                except AssertionError:
                    await self.log(f'❌ {i+1} ответ не является голосовым')
                    await self.log(f'❌ {self.peer} не удовлетворяет проверке:\n<code>{query}</code>')
                    return False

        # Проверяем содержание сообщений
        for check in expected_content:
            response_index, operator, content = check
            if operator == 'has':
                # has применим только к текстовым сообщениям - проверяем
                try:
                    assert response.messages[response_index].text
                except AssertionError:
                    await self.log(f'❌ Оператор has работает только с текстовыми ответами')
                    await self.log(f'❌ {self.peer} не удовлетворяет проверке:\n<code>{query}</code>')
                    return False
                # проверяем вхождение строки
                try:
                    string = content.replace("'", '')
                    assert string in response.messages[response_index].text
                    await self.log(f'✅ {response_index+1} ответ содержит "{string}"')
                except AssertionError:
                    await self.log(f'❌ {response_index+1} ответ не содержит "{string}"')
                    await self.log(f'❌ {self.peer} не удовлетворяет проверке:\n<code>{query}</code>')
                    return False

        await self.log(f'✅ {self.peer} удовлетворяет проверке:\n<code>{query}</code>')
        return True

    async def run_dev_query(self, query, clear_chat = False):
        parsed_query = self._parse_query(query)
        await self.run_query(parsed_query)


    def _parse_query(self, query):
        # Разбиваем строку на лексемы
        lexemes = self._get_lexemes(query)
        print(lexemes)
        # Ищем стрелку ->
        try:
            arrow_index = lexemes.index('->')
        except ValueError:
            return ('error', f'❌ Некорректная проверка: отсутствует символьный оператор <code>-></code>\n<code>{query}</code>')

        # Парсим input
        action_value = lexemes[:arrow_index]
        # Проверяем количество аругментов - должно быть 2: action и value
        if len(action_value) != 2:
            return ('error', f'❌ Некорректная проверка: слишком много аргументов\n<code>{query}</code>')

        # Проверяем action
        action = action_value[0]
        if action not in self.actions:
            return ('error', f'❌ Некорректная проверка: <code>{action}</code> - неверный тип действия\n<code>{query}</code>')

        value = action_value[-1]
        # Парсим value
        if action == 'type':
            if value[0] == '/':
                parsed_input = ('cmd', value[1:])
            else:
                parsed_input = ('text', value)
        elif action == 'press':
            return ('error', f'❌ Некорректная проверка: <code>{action}</code> - действие пока не поддерживается\n<code>{query}</code>')

        # Парсим expected_output
        expected_output = lexemes[arrow_index:]

        expected_types = []
        expected_content = []

        new_check = []
        waiting_for_value = False
        for i, lexeme in enumerate(expected_output):
            if waiting_for_value:
                new_check.append(lexeme)
                expected_content.append(new_check)
                new_check = []
                waiting_for_value = False
                continue
            if lexeme in self.types:
                expected_types.append(lexeme)
                continue
            if lexeme in self.operators:
                operator = lexeme
                if len(expected_types) == 0:
                    response_index = 0
                else:
                    response_index = len(expected_types) - 1
                new_check = [response_index, operator]
                waiting_for_value = True
                continue

        return ('success', (parsed_input, expected_types, expected_content))

    def _get_lexemes(self, query):
        # Работаем с одинарными кавычками
        query = query.replace('"', "'")
        lexemes = []
        lexeme = ''
        string_started = False
        for i, char in enumerate(query):
            # Пропускаем кавычки и закрываем/открываем строку
            if char == "'":
                # Для строк в лексему добавляем кавчку
                if string_started:
                    lexemes.append(f"'{lexeme}'")
                    lexeme = ''
                string_started = not string_started
                continue
            # Лексемы разделяются пробелами, в строках пробелы допустимы
            if char == ' ' and not string_started:
                if not lexeme.isspace() and not lexeme == '': lexemes.append(lexeme)
                lexeme = ''
                continue
            lexeme += char
            # Руками добавляем последнюю лексему, так как она не закрывается пробелом
            if i == len(query)-1: lexemes.append(lexeme)
        return lexemes
