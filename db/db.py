import aiosqlite
from aiogram.types import Message, ChatMemberUpdated, CallbackQuery
from sqlite3 import Error
import asyncio


__all__ = [
    'check_exist_user', 'update_activity_user', 'insert_new_user',
    'update_status_user', 'create_session', 'check_active_session',
    'create_attempt', 'get_active_session', 'get_letters',
    'get_letters_excluded', 'insert_chars_to_attempt', 'get_length_word'
    ]

async def check_exist_user(database: str, id: int) -> bool:
    '''
    Функция проверяет существование пользователя в базе
    '''
    try:
        async with aiosqlite.connect(database) as conn:
            cursor = await conn.execute(f'SELECT tg_id FROM users WHERE tg_id={id}')
            if await cursor.fetchone():
                return True
            else:
                return False
    except Error:
        print(Error)


async def check_status_user(database: str, id: int) -> bool:
    '''
    Функция проверяет состояние взаимодействия бота с пользователем в базе (заблокирован бот или нет)
    '''
    try:
        async with aiosqlite.connect(database) as conn:
            cursor = await conn.execute(f'SELECT status FROM users WHERE tg_id={id}')
            res = await cursor.fetchone()
            if res and res[0] == 1:
                return True
            else:
                return False
    except Error:
        print(Error)


async def insert_new_user(database: str, message: Message):
    '''
    Функция добавлявет нового пользователя в базу
    '''
    try:
        async with aiosqlite.connect(database) as conn:
            await conn.execute(f'INSERT INTO users (tg_id, status, registered, activity) VALUES ({message.from_user.id}, 1, datetime("now"), datetime("now"))')
            await conn.commit()
    except Error:
        print(Error)


async def update_activity_user(database: str, message: Message):
    '''
    Функция обновляет данные пользователя после команды /start
    '''
    try:
        async with aiosqlite.connect(database) as conn:
            await conn.execute(f'UPDATE users SET status=1, activity=datetime("now") WHERE tg_id={message.from_user.id}')
            await conn.commit()
    except Error:
        print(Error)


async def update_status_user(database: str, update: Message|ChatMemberUpdated):
    '''
    Функция обновляет данные пользователя после команды /start
    '''
    try:
        async with aiosqlite.connect(database) as conn:
            await conn.execute(f'UPDATE users SET status=0 WHERE tg_id={update.from_user.id}')
            await conn.commit()
    except Error:
        print(Error)


async def create_session(database: str, callback: CallbackQuery):
    '''
    Функция создания сессии по поиску слова
    '''
    try:
        user = callback.from_user.id
        word_len = int(callback.data.split('_')[-1])
        async with aiosqlite.connect(database) as conn:
            await conn.execute(f'INSERT INTO sessions (tg_id, started, active, word_len) VALUES ({user}, datetime("now"), 1, {word_len})')
            await conn.commit()
    except Error:
        print(Error)


async def check_active_session(database: str, message: Message) -> bool:
    '''
    Проверка наличия активной сессии
    '''
    try:
        async with aiosqlite.connect(database) as conn:
            cursor = await conn.execute(f'SELECT active FROM sessions WHERE tg_id={message.from_user.id}')
            res = await cursor.fetchone()
            print(res)
            if res and res[0] == 1:
                print('True')
                return True
            else:
                print('False')
                return False
    except aiosqlite.Error as e:
        print(e)


async def create_attempt(database: str, callback: CallbackQuery):
    '''
    Функция создания попытки подбора слов
    '''
    query = f'INSERT INTO attempts (session_id, attempt_number, message_id) VALUES ((SELECT id FROM sessions WHERE tg_id={callback.from_user.id} AND active=1), (SELECT count() FROM attempts WHERE session_id=(SELECT id FROM sessions WHERE tg_id={callback.from_user.id} AND active=1)), {callback.message.message_id})'
    try:
        async with aiosqlite.connect(database) as conn:
            await conn.execute(query)
            await conn.commit()
    except aiosqlite.Error as e:
        print(e)


async def get_active_session(database: str, callback: CallbackQuery) -> int:
    try:
        async with aiosqlite.connect(database) as conn:
            cursor = await conn.execute(f'SELECT id FROM sessions WHERE tg_id={callback.from_user.id}')
            res = await cursor.fetchone()
            return res[0]
    except aiosqlite.Error as e:
        print(e)


async def get_letters(database: str, callback: CallbackQuery):
    try:
        suf, let = callback.data.split('_')
        if suf == 'rem':
            table = 'excluded'
        else:
            table = 'included'
        session_id = await get_active_session(database, callback)
        async with aiosqlite.connect(database) as conn:
            cursor = await conn.execute(f'SELECT chars_{table} FROM attempts WHERE session_id={session_id} AND attempt_number=(SELECT max(attempt_number) FROM attempts WHERE session_id={session_id})')
            result = await cursor.fetchone()
        return result[0]
    except aiosqlite.Error as e:
        print(e)


async def get_letters_excluded(database: str, callback: CallbackQuery):
    try:
        suf, let = callback.data.split('_')
        session_id = await get_active_session(database, callback)
        async with aiosqlite.connect(database) as conn:
            cursor = await conn.execute(f'SELECT chars_excluded FROM attempts WHERE session_id={session_id} AND attempt_number=(SELECT max(attempt_number) FROM attempts WHERE session_id={session_id})')
            result = await cursor.fetchone()
        return result[0]
    except aiosqlite.Error as e:
        print(e)


async def get_length_word(database: str, callback: CallbackQuery):
    try:
        async with aiosqlite.connect(database) as conn:
            cursor = await conn.execute(f'SELECT word_len FROM sessions WHERE tg_id={callback.from_user.id} and active=1')
            result = await cursor.fetchone()
        return result[0]
    except aiosqlite.Error as e:
        print(e)


async def insert_chars_to_attempt(database: str, callback: CallbackQuery, letters: str):
    try:
        if 'rem' in callback.data:
            field = 'excluded'
        else:
            field = 'included'
        session_id = await get_active_session(database, callback)
        async with aiosqlite.connect(database) as conn:
            await conn.execute(f'UPDATE attempts SET chars_{field}="{letters}" WHERE session_id={session_id}')
            await conn.commit()
    except aiosqlite.Error as e:
        print(e)

'''
INSERT INTO users (tg_id, status, registered, activity) VALUES (173718058, 1, datetime('now'), datetime('now'))

INSERT INTO sessions (tg_id, started, active) VALUES (133073976, datetime('now'), 1)

SELECT tg_id FROM users WHERE tg_id=1737180589

UPDATE users SET status=0 WHERE tg_id=133073976


INSERT INTO attempts (session_id, attempt_number) VALUES 
    ((SELECT id FROM sessions WHERE tg_id=133073976 AND active=1), 
    (SELECT count() FROM attempts WHERE session_id=(SELECT id FROM sessions WHERE tg_id=133073976 AND active=1)))


SELECT chars_excluded FROM attempts WHERE session_id=4 AND attempt_number=(SELECT max(attempt_number) FROM attempts WHERE session_id=4)
'''


# if __name__ == '__main__':
#     asyncio.run(check_status_user('database.db', 133073976))
