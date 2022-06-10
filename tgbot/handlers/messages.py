messages = {
    'start_message':"""
Привет!

Этот бот занимается тестирование других телеграм ботов.
В данный момент он прикреплен к боту @ruricbot.

Здесь можно тестировать бота используя специальный язык проверок.
Также можно создать тесты - группы проверок, которые будут выполнятся последовательно.

/help - подробнее про язык проверок
/query - выполнить единичную проверку
/tests - составить тесты (группы проверок)
""",
    'instruction_message': """
<b>TgTestLang</b>

Используем язык описания проверок.

Структура проверки:
<code>action input -> expected_output -> expected_output -> ...</code>

Примеры проверок:

<code>type /start -> text(1) has 'Я Рюрик - Король Русов'</code>
<code>type /help -> text(1) has 'СЛАВА РУСАМ! И СРАМ ЕЩЁ!'</code>
<code>type /goblin -> video(1) -> text(1)</code>
<code>type Test text -> voice(1)</code>
<code>type /cancel -> pass</code>


Сначала задаём действие (<code>action</code>). Иx 2 вида:
1) Ввод текста <code>type</code>
2) Нажатие на кнопку <code>press</code> (coming soon)

Затем указываем входные данные (<code>input</code>). Они бывают 3 видов:
1) Команда <code>/example</code>
2) Пользовательский текст <code>example</code>
3) Нажатие на inline-кнопку (coming soon)


Далее пишем символьный оператор <code>-></code>


После этого описываем ожидаемый от бота ответ (<code>expected_output</code>):
1) Сначала описываем тип ответа, в скобочках количество ожидаемых сообщений:
<code>text(2)</code>
2) Оператор <code>has</code> проверяет содержится ли в тексте указанная строка:
<code>type /help -> text(1) has 'Help message'</code>
3) Оператор <code>pass</code> означает, что <code>expected_output</code> может быть любой

Можно описывать цепочки ответов
<code>type /goblin -> video(1) -> text(1)</code>

Используем проверку <code>type /cancel -> pass</code> чтобы вывести бота из стейта (если такая команда у него предусмотрена конечно)

/query - выполнить единичную проверку
/tests - составить тесты (группы проверок)
""",

    'query_instruction': """
Введите проверку для <b>{bot_name}</b>
""",
    'query_examples':"""
Примеры проверок:
<code>type /start -> text(1) has 'Я Рюрик - Король Русов'</code>
<code>type /help -> text(1) has 'СЛАВА РУСАМ! И СРАМ ЕЩЁ!'</code>
<code>type /goblin -> video(1) -> text(1)</code>
<code>type Test text -> voice(1)</code>
<code>type /cancel -> pass</code>
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
