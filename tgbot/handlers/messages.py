messages = {
    'start_message':"""
Привет!

Этот бот занимается тестирование других телеграм ботов.
В данный момент он прикреплен к боту @ruricbot.

Здесь можно тестировать бота используя специальный язык проверок.
Также можно создать тесты - группы проверок, которые будут выполнятся последовательно.

/basics - примеры использования
/query - выполнить единичную проверку
/tests - составить тесты (группы проверок)
""",
    'instruction_message': """
<b>TgTestLang</b>

Структура проверки:
<code>action value -> expected_output -> expected_output -> ...</code>

Сначала задаём действие (<code>action</code>). Иx 2 вида:
1) Ввод текста <code>type</code>
2) Нажатие на кнопку <code>press</code> (coming soon)

Затем указываем входные данные (<code>value</code>). Они бывают 3 видов:
1) Команда <code>/example</code>
2) Пользовательский текст <code>'example'</code>
3) Нажатие на inline-кнопку (coming soon)

Далее пишем символьный оператор <code>-></code>

После этого описываем ожидаемый от бота ответ (<code>expected_output</code>):
1) Сначала описываем тип ответа, в скобочках можно задать количество ожидаемых сообщений:
<code>text(2)</code>
2) Оператор <code>has</code> проверяет содержится ли в тексте указанная строка:
<code>type /help -> text() has 'Hello! This is help message.'</code>
3) Оператор <code>pass</code> означает, что <code>expected_output</code> может быть любой

Используем проверку <code>type /cancel -> pass</code> чтобы вывести бота из стейта (если такая команда у него предусмотрена конечно)

/basics - примеры использования
/query - выполнить единичную проверку
/tests - составить тесты (группы проверок)
""",

    'query_instruction': """
Введите проверку для <b>{bot_name}</b>
""",
    'query_examples':"""
<b>Примеры проверок:</b>

<code>type /help -> text(1) has 'Hello! This a is help message.'</code>
Проверяет содержится ли в ответе на команду <code>/help</code> текст 'Hello! This is help message'.

<code>type /goblin -> video(1) text(1)</code>
Проверяет выводится ли по команде <code>/goblin</code> сначало видео, а потом текстовое сообщение.

<code>type 'Hello' -> voice(1)</code>
Проверяет выводится ли при наборе текста 'Hello' голосовое сообщение

<code>type /cancel -> pass</code>
Вводит команду <code>/cancel</code> и ничего не проверяет (сбрасывает state)

/help - подробнее
""",
    'tests_list_empty':"""
Тестов для <b>{bot_name}</b> пока не создано.
""",
    'tests_list_title':"""
Тесты для {bot_name}:

""",
    'test_created':"""
Тест <b>{test_name}</b> для {bot_name} создан.
""",
    'test_deleted':"""
Тест <b>{test_name}</b> для {bot_name} был удален.
""",
    'test_queries_list':"""
Проверки в тесте <b>{test_name}</b> для {bot_name}:
""",
    'test_queries_list_empty':"""
Тест <b>{test_name}</b> для {bot_name} пока пустой.
Добавьте первую проверку.
""",
    'test_queries_list_title':"""
 Тест <b>{test_name}</b> для {bot_name}:
""",
    'add_query_instruction': """
Добавьте проверку в тест <b>{test_name}</b> для <b>{bot_name}</b>:
""",
    'query_added':"""
Проверка: {query}
добавлена в тест <b>{test_name}</b> для <b>{bot_name}</b>.
""",
    'query_deleted':"""
Проверка: {query}
удалена из теста <b>{test_name}</b> для <b>{bot_name}</b>.
"""
}
