from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.utils.exceptions import MessageNotModified
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from contextlib import suppress

from tgbot.services.repository import Repo

from tgbot.handlers.messages import messages

async def user_start(m: Message, repo: Repo):
    await repo.add_user(m.from_user.id)
    await m.reply("Привет!")

async def show_help(m: Message):
    await m.answer(messages['instruction_message'])

# Единичная проверка
async def run_query(m: Message, repo: Repo):
    await m.answer(messages['query_instruction'].format(bot_name = await repo.get_bot_name(m.from_user.id)) + messages['query_examples'])

# Показываем все тесты
async def show_tests(m: Message, state: FSMContext, repo: Repo):
    await state.finish()
    bot_name = await repo.get_bot_name(m.from_user.id)
    tests = await repo.get_tests(bot_name)
    keyboard = InlineKeyboardMarkup(row_width=1)
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
    keyboard = InlineKeyboardMarkup(row_width=1)
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


# Меню теста, добавляем проверки, удаляем проверки, можем пойти назад к смиску тестов, запускам тест
async def edit_test(m: Message, state: FSMContext, repo: Repo):
    test_name = m.text[6:]
    test_name, bot_name, queries = await repo.get_test(test_name)

    await state.update_data(test_name=test_name)
    await EditTest.choosing_option.set()

    keyboard = InlineKeyboardMarkup(row_width=2)

    # Если ещё нет проверок, обовещаем об этом, оставляем только кнопу добавить и назад
    if queries == None:
        keyboard.insert(InlineKeyboardButton('🔙', callback_data='back_to_tests'))
        keyboard.insert(InlineKeyboardButton('➕', callback_data='add_query'))
        await m.answer(messages['test_queries_list_empty'].format(test_name=test_name, bot_name=bot_name), reply_markup=keyboard)
    else:
        keyboard.insert(InlineKeyboardButton('▶️', callback_data='run_test'))
        keyboard.insert(InlineKeyboardButton('➕', callback_data='add_query'))
        keyboard.insert(InlineKeyboardButton('🔙', callback_data='back_to_tests'))
        keyboard.insert(InlineKeyboardButton('➖', callback_data='delete_query'))
        queries_list = [f'{i+1}) {query}' for i, query in enumerate(queries.split('\n'))]
        await m.answer(messages['test_queries_list_title'].format(test_name=test_name, bot_name=bot_name) +'\n'+'\n'.join(queries_list), reply_markup=keyboard)

async def add_query(q: CallbackQuery, repo: Repo):
    return
async def delete_query(m: Message, repo: Repo):
    return
async def run_test(m: Message, repo: Repo):
    return
# Регистрируем хендлеры
def register_user(dp: Dispatcher):
    # Общие
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(show_help, commands=["help"], state="*")
    dp.register_message_handler(run_query, commands=["query"], state="*")
    # Тесты
    dp.register_message_handler(show_tests, commands=["tests"], state="*")
    dp.register_callback_query_handler(back_to_tests, lambda c: c.data in ['back_to_tests'], state="*")
    dp.register_callback_query_handler(name_test, lambda c: c.data in ['create_test'], state="*")
    dp.register_message_handler(create_test, state=NameTest.waiting_for_test_name)
    dp.register_message_handler(edit_test, Text(startswith='/goto'), state="*")

# Стейты
class NameTest(StatesGroup):
    waiting_for_test_name = State()

class EditTest(StatesGroup):
    choosing_option = State()
    waiting_for_query = State()

class StackQuery(StatesGroup):
    waiting_for_query = State()
