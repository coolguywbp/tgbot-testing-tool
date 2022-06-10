from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from contextlib import suppress

from tgbot.services.repository import Repo
from tgbot.services.test import Test

from tgbot.handlers.messages import messages

async def user_start(m: Message, state: FSMContext, repo: Repo):
    await state.finish()
    await repo.add_user(m.from_user.id)
    await m.reply(messages['start_message'])

async def show_basics(m: Message, state: FSMContext,):
    await state.finish()
    await m.answer(messages['query_examples'])

async def show_help(m: Message, state: FSMContext,):
    await state.finish()
    await m.answer(messages['instruction_message'])

# Единичная проверка
async def setup_single_query(m: Message, state: FSMContext, repo: Repo):
    await state.finish()
    await SingleQuery.waiting_for_query.set()
    await m.answer(messages['query_examples'])
    await m.answer(messages['query_instruction'].format(bot_name = await repo.get_bot_name(m.from_user.id)))

async def run_single_query(m: Message, state: FSMContext, test: Test):
    await state.finish()
    query = m.text
    test_log = test.run_query_demo(query)
    await m.answer(test_log)
# Показываем все тесты
async def show_tests(m: Message, state: FSMContext, repo: Repo):
    await state.finish()
    bot_name = await repo.get_bot_name(m.from_user.id)
    tests = await repo.get_tests(bot_name)
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.insert(InlineKeyboardButton('➖', callback_data='delete_test'))
    keyboard.insert(InlineKeyboardButton('➕', callback_data='create_test'))
    if len(tests) == 0:
        await m.answer(messages['tests_list_empty'].format(bot_name=bot_name), reply_markup=keyboard)
    else:
        tests_list = []
        for test in tests:
            if test[2] == None:
                queries_len = 0
            else:
                queries_len = len(test[2].split('\n'))
            tests_list.append(f'<b>{str(test[0])}</b>({str(queries_len)})     /goto_{str(test[0])}')
        await m.answer(messages['tests_list_title'].format(bot_name=bot_name) + '\n'.join(tests_list), reply_markup=keyboard)

async def back_to_tests(q: CallbackQuery, state: FSMContext, repo: Repo):
    await state.finish()
    bot_name = await repo.get_bot_name(q.message.chat.id)
    tests = await repo.get_tests(bot_name)
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.insert(InlineKeyboardButton('➖', callback_data='delete_test'))
    keyboard.insert(InlineKeyboardButton('➕', callback_data='create_test'))
    if len(tests) == 0:
        response = messages['tests_list_empty'].format(bot_name=bot_name)
    else:
        tests_list = []
        for test in tests:
            if test[2] == None:
                queries_len = 0
            else:
                queries_len = len(test[2].split('\n'))
            tests_list.append(f'<b>{str(test[0])}</b>({str(queries_len)})     /goto_{str(test[0])}')
        response = messages['tests_list_title'].format(bot_name=bot_name) + '\n'.join(tests_list)
    with suppress(MessageNotModified):
        await q.message.edit_text(response)
        await q.message.edit_reply_markup(reply_markup = keyboard)

# После нажатия на ➕ просим назвать тест
async def name_test(q: CallbackQuery, repo: Repo):
    bot_name = await repo.get_bot_name(q.message.chat.id)
    with suppress(MessageNotModified):
        await q.message.edit_text(f'Назовите новый тест для {bot_name}:')
        await q.message.edit_reply_markup(reply_markup = InlineKeyboardMarkup())
    await NameTest.waiting_for_test_name.set()

# Создаём тест и просим ввести первую проверку
async def create_test(m: Message, state: FSMContext, repo: Repo):
    await state.finish()

    test_name = m.text
    bot_name = await repo.get_bot_name(m.from_user.id)
    await repo.create_test(test_name, bot_name)

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.insert(InlineKeyboardButton('🔙', callback_data='back_to_tests'))

    await m.answer(messages['test_created'].format(test_name=test_name, bot_name = bot_name))
    await show_tests(m, state, repo)
# После нажатия на ➖ вызываем кнопи для удаления
async def call_delete_test_buttons(q: CallbackQuery, repo: Repo):
    bot_name = await repo.get_bot_name(q.message.chat.id)
    tests = await repo.get_tests(bot_name)
    keyboard = InlineKeyboardMarkup(row_width=1)
    for test in tests:
        keyboard.insert(InlineKeyboardButton(test[0], callback_data=cb_delete_test.new(name=test[0])))
    keyboard.insert(InlineKeyboardButton('🔙', callback_data='back_to_tests'))
    await q.message.edit_reply_markup(reply_markup = keyboard)

# Удаляем тест
async def delete_test(q: CallbackQuery, callback_data: dict, state: FSMContext, repo: Repo):
    test_name = callback_data["name"]
    bot_name = await repo.get_bot_name(q.message.chat.id)
    await repo.delete_test(test_name, bot_name)

    await q.message.answer(messages['test_deleted'].format(test_name=test_name, bot_name = bot_name))
    await show_tests(q.message, state, repo)

# Меню теста, добавляем проверки, удаляем проверки, можем пойти назад к смиску тестов, запускам тест
async def edit_test(m: Message, state: FSMContext, repo: Repo):
    async with state.proxy() as data:
        if 'test_name' in data:
            test_name = data['test_name']
        else:
            test_name = m.text[6:]
            data['test_name'] = test_name

    test_name, bot_name, queries = await repo.get_test(test_name)
    await EditTest.choosing_option.set()

    keyboard = InlineKeyboardMarkup(row_width=2)

    # Если ещё нет проверок, обовещаем об этом, оставляем только кнопу добавить и назад
    if queries == None:
        keyboard.insert(InlineKeyboardButton('🔙', callback_data='back_to_tests'))
        keyboard.insert(InlineKeyboardButton('➕', callback_data='setup_query'))
        await m.answer(messages['test_queries_list_empty'].format(test_name=test_name, bot_name=bot_name), reply_markup=keyboard)
    else:
        keyboard.insert(InlineKeyboardButton('▶️', callback_data='run_test'))
        keyboard.insert(InlineKeyboardButton('➕', callback_data='setup_query'))
        keyboard.insert(InlineKeyboardButton('🔙', callback_data='back_to_tests'))
        keyboard.insert(InlineKeyboardButton('➖', callback_data='delete_query'))
        queries_list = [f'{i+1}) {query}' for i, query in enumerate(queries.split('\n'))]
        await m.answer(messages['test_queries_list_title'].format(test_name=test_name, bot_name=bot_name) +'\n'+'\n'.join(queries_list), reply_markup=keyboard)

# Запрашиваем проверку для добавления в тест
async def setup_query(q: CallbackQuery, state: FSMContext, repo: Repo):
    bot_name = await repo.get_bot_name(q.message.chat.id)
    async with state.proxy() as data:
        test_name = data['test_name']
    await EditTest.waiting_for_query.set()
    await q.message.answer(messages['query_examples'])
    await q.message.answer(messages['add_query_instruction'].format(test_name=test_name, bot_name=bot_name))

# Добавляем проверку в тест
async def add_query(m: Message, state: FSMContext, repo: Repo):
    query = m.text
    bot_name = await repo.get_bot_name(m.from_user.id)
    async with state.proxy() as data:
        test_name = data['test_name']
    await repo.add_query(test_name, bot_name, m.text)
    await m.answer(messages['query_added'].format(test_name=test_name, bot_name=bot_name, query=query))
    await edit_test(m, state, repo)

async def delete_query(q: CallbackQuery, state: FSMContext, repo: Repo):
    bot_name = await repo.get_bot_name(q.message.chat.id)
    async with state.proxy() as data:
        test_name = data['test_name']
    deleted_query = await repo.delete_last_query(test_name, bot_name)
    await q.message.answer(messages['query_deleted'].format(test_name=test_name, bot_name=bot_name, query=deleted_query))
    await edit_test(q.message, state, repo)

async def run_test(q: CallbackQuery, repo: Repo):
    return
# Регистрируем хендлеры
def register_user(dp: Dispatcher):
    # Общие
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(show_basics, commands=["basics", "examples"], state="*")
    dp.register_message_handler(show_help, commands=["help"], state="*")
    # Единичная проверка
    dp.register_message_handler(setup_single_query, commands=["query"], state="*")
    dp.register_message_handler(run_single_query, state=SingleQuery.waiting_for_query)
    # Тесты
    dp.register_message_handler(show_tests, commands=["tests"], state="*")
    dp.register_callback_query_handler(back_to_tests, lambda c: c.data in ['back_to_tests'], state="*")
    dp.register_callback_query_handler(name_test, lambda c: c.data in ['create_test'], state="*")
    dp.register_message_handler(create_test, state=NameTest.waiting_for_test_name)
    dp.register_callback_query_handler(call_delete_test_buttons, lambda c: c.data in ['delete_test'])
    dp.register_callback_query_handler(delete_test, cb_delete_test.filter(), state="*")
    dp.register_message_handler(edit_test, Text(startswith='/goto'), state="*")
    dp.register_callback_query_handler(setup_query, lambda c: c.data in ['setup_query'], state=EditTest.choosing_option)
    dp.register_callback_query_handler(delete_query, lambda c: c.data in ['delete_query'], state=EditTest.choosing_option)
    dp.register_message_handler(add_query, state=EditTest.waiting_for_query)

# Стейты
class NameTest(StatesGroup):
    waiting_for_test_name = State()

class EditTest(StatesGroup):
    choosing_option = State()
    waiting_for_query = State()

class SingleQuery(StatesGroup):
    waiting_for_query = State()

# Фабрики колбэков
cb_delete_test = CallbackData("testnum", "name")
