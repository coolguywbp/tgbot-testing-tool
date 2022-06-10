messages = {
    'instruction_message': """
<b>TestLang</b>

Используем язык описания проверок.

Структура проверки:
<code>input -> expected output</code>

Примеры проверок:

<code>/start -> text(1) has 'Я Рюрик - Король Русов'</code>
<code>/help -> text(1) has 'СЛАВА РУСАМ! И СРАМ ЕЩЁ!'</code>
<code>/goblin -> video(1) text(1)</code>
<code>Test text -> voice(1)</code>
<code>/cancel -> pass</code>


Сначала пишем <code>input</code>. Они бывают 3 видов:

1) Команда <code>/example</code>
2) Пользовательский текст <code>example</code>
3) Нажатие на inline-кнопку (coming soon)


Далее ставим <code>-></code>


После этого описываем <code>expected output</code>:

1) Сначала описываем тип ответа, в скобочках количество ожидаемых сообщений:
<code>text(2)</code>
Можно указать несколько типов ответа подряд:
<code>video(1) text(1)</code>
2) Оператор <code>has</code> проверяет содержится ли в тексте указанная строка:
<code>/help -> text(1) has 'Help message'</code>
3) Оператор <code>pass</code> означает, что <code>output</code> может быть любой


Изпользуем проверку <code>/cancel -> pass</code> чтобы вывести бота из стейта.

/query - выполнить единичную проверку
/tests - составить тесты (группы проверок)
""",

    'query_instruction': """
Введите проверку для <b>{bot_name}</b>
""",
    'query_examples':"""
Примеры проверок:
<code>/start -> text(1) has 'Я Рюрик - Король Русов'</code>
<code>/help -> text(1) has 'СЛАВА РУСАМ! И СРАМ ЕЩЁ!'</code>
<code>/goblin -> video(1) text(1)</code>
<code>Test text -> voice(1)</code>
<code>/cancel -> pass</code>
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
    'test_queries_list':"""
Проверки в тесте <b>{test_name}</b> для {bot_name}:
""",
    'test_queries_list_empty':"""
Тест <b>{test_name}</b> для {bot_name} пока пустой.
Добавте перую проверку.
""",
    'test_queries_list_title':"""
 Тест <b>{test_name}</b> для {bot_name}:
""",
}
