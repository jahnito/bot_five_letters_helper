from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from aiogram.types import Message, ChatMemberUpdated, CallbackQuery
from aiogram import F
from pprint import pprint
from config import Config
from db import *
from filters import *
from lexicon import RU


from kb import gen_kb_letters


CONF = Config()
_db = CONF.db['db_file']
bot = Bot(token=CONF.token)
dp = Dispatcher()


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    # pprint(message.model_dump_json(indent=4, exclude_none=True))
    if await check_exist_user(_db, message.from_user.id):
        await update_activity_user(_db, message)
        await message.answer(RU['greeting_repeat'])
    else:
        await insert_new_user(_db, message)
        await message.answer(RU['greeting'])


@dp.message(Command(commands=['guess']))
async def process_help_command(message: Message):
    # pprint(message.model_dump_json(indent=4, exclude_none=True))
    if await check_active_session(_db, message):
        print('Сессия запущена')
    else:
        await create_session(_db, message) # создаем сессию
        await create_attempt(_db, message) # создаем первую попытку
        await message.answer(
            text='Сессия подбора слова запущена, выбери буквы которых нет в слове',
            reply_markup=gen_kb_letters('rem')
            )


@dp.callback_query(IsRemoveLetter())
async def callback_test(callback: CallbackQuery, let):
    await callback.answer(f'Для исключения выбрана буква *{let}*')
    chars_excluded = await get_letters(_db, callback)
    if chars_excluded:
        letters = chars_excluded + let
    else:
        letters = let
    await insert_chars_to_attempt(_db, callback, letters)
    await callback.message.edit_text(
        f'Для исключения выбраны буквы:\n{", ".join(letters)}\n'
        'для продолжения нажмите Принять',
        reply_markup=callback.message.reply_markup)
    # print(letters)


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    pprint(message.model_dump_json(indent=4, exclude_none=True))
    await message.answer('help command')


@dp.my_chat_member()
async def all(chatmemberupdated: ChatMemberUpdated):
    # pprint(message.model_dump_json(indent=4, exclude_none=True))
    if await check_exist_user(_db, chatmemberupdated.from_user.id) and chatmemberupdated.new_chat_member.status == 'kicked':
        await update_status_user(_db, chatmemberupdated)
        print('Бот заблокирован')
    # await message.answer('my_chat_member')


if __name__ == "__main__":
    dp.run_polling(bot)
