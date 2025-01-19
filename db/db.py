import aiosqlite
from aiogram.types import Message, ChatMemberUpdated
from sqlite3 import Error
import asyncio


__all__ = ['check_exist_user', 'update_activity_user', 'insert_new_user',
           'update_status_user',]

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
            print(res)
            if res and res[0] == 1:
                print('True')
                return True
            else:
                print('False')
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


'''
INSERT INTO users (tg_id, status, registered, activity) VALUES (173718058, 1, datetime('now'), datetime('now'))

SELECT tg_id FROM users WHERE tg_id=1737180589

UPDATE users SET status=0 WHERE tg_id=133073976
'''


if __name__ == '__main__':
    asyncio.run(check_status_user('database.db', 133073976))
