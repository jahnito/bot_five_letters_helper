import aiosqlite
from aiogram.types import Message, ChatMemberUpdated, CallbackQuery
from sqlite3 import Error
import asyncio


__all__ = [
    'check_exist_user', 'update_activity_user', 'insert_new_user',
    'update_status_user', 'create_session', 'check_active_session',
    'create_attempt', 'get_active_session', 'get_letters',
    'get_letters_excluded', 'get_letters_included',
    'insert_chars_to_attempt', 'get_length_word',
    'get_pos_letters', 'insert_positions_to_attempt',
    'reset_positions_to_attempt', 'get_all_data_attempt', 'get_words_from_dict',
    'insert_filtered_dict', 'get_words_from_filtered_dict',
    'count_filtered_words', 'end_session', 'create_attempt_next',
    'delete_filtered_dict', 'get_current_attempt', 'get_random_word',
    'get_time_from_last', 'get_message_id_attempt', 'get_len_and_status',
    'insert_session_word'
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
        return False


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
        return False


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
            cursor = await conn.execute(f'SELECT active FROM sessions WHERE tg_id={message.from_user.id} ORDER BY active DESC limit 1')
            res = await cursor.fetchone()
            if res and res[0] == 1:
                return True
            else:
                return False
    except aiosqlite.Error as e:
        print(e)
        return False


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


async def create_attempt_next(database: str, callback: CallbackQuery, data: dict):
    '''
    Функция переносит данный из предыдущей попытки и создает новую, для улучшенной фильтрации слов
    '''
    if data.get('ex'):
        excluded = data['ex']
    else:
        excluded = ''

    if data.get('in'):
        included = data['in']
    else:
        included = ''

    if data.get('ip'):
        in_pos = data['ip']
    else:
        in_pos = ''

    if data.get('np'):
        non_pos = data['np']
    else:
        non_pos = ''

    query = f'INSERT INTO attempts \
                (session_id, message_id, chars_excluded, chars_included, chars_non_in_pos, chars_in_pos, attempt_number) \
            VALUES ( \
                (SELECT id FROM sessions WHERE tg_id={callback.from_user.id} AND active=1), \
            {callback.message.message_id}, \
            "{excluded}", \
            "{included}", \
            "{non_pos}", \
            "{in_pos}", \
            (SELECT count() FROM attempts WHERE session_id=(SELECT id FROM sessions WHERE tg_id={callback.from_user.id} AND active=1)))'
    try:
        async with aiosqlite.connect(database) as conn:
            await conn.execute(query)
            await conn.commit()
    except aiosqlite.Error as e:
        print(e)


async def delete_filtered_dict(database: str, callback: CallbackQuery):
    '''
    Функция удаления отфильтрованных словарей, удаляет все записи по tg_id
    '''
    query = f'DELETE FROM filtered_dicts WHERE tg_id={callback.from_user.id}'
    try:
        async with aiosqlite.connect(database) as conn:
            await conn.execute(query)
            await conn.commit()
    except aiosqlite.Error as e:
        print(e)


async def get_active_session(database: str, callback: CallbackQuery, active=1) -> int:
    try:
        async with aiosqlite.connect(database) as conn:
            cursor = await conn.execute(f'SELECT id FROM sessions WHERE tg_id={callback.from_user.id} AND active={active} ORDER BY id DESC LIMIT 1')
            res = await cursor.fetchone()
            return res[0]
    except aiosqlite.Error as e:
        print(e)
        return None


async def get_current_attempt(database: str, callback: CallbackQuery):
    query = f'SELECT max(attempt_number) FROM attempts WHERE session_id=(SELECT id FROM sessions WHERE tg_id={callback.from_user.id} AND active=1) '
    try:
        async with aiosqlite.connect(database) as conn:
            cursor = await conn.execute(query)
            res = await cursor.fetchone()
            return res[0]
    except aiosqlite.Error as e:
        print(e)


async def get_message_id_attempt(database: str, message: Message|CallbackQuery):
    query = f'SELECT message_id FROM attempts WHERE session_id=(SELECT id FROM sessions WHERE tg_id={message.from_user.id} AND active=1)'
    try:
        async with aiosqlite.connect(database) as conn:
            cursor = await conn.execute(query)
            res = await cursor.fetchone()
            return res[0]
    except aiosqlite.Error as e:
        print(e)


async def get_letters(database: str, callback: CallbackQuery):
    try:
        suf, let = callback.data.split('_')
        if (suf == 'rem' and len(let) == 1) or suf == 'next':
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


async def get_letters_included(database: str, callback: CallbackQuery):
    try:
        suf, let = callback.data.split('_')
        session_id = await get_active_session(database, callback)
        async with aiosqlite.connect(database) as conn:
            cursor = await conn.execute(f'SELECT chars_included FROM attempts WHERE session_id={session_id} AND attempt_number=(SELECT max(attempt_number) FROM attempts WHERE session_id={session_id})')
            result = await cursor.fetchone()
        return result[0]
    except aiosqlite.Error as e:
        print(e)


async def get_length_word(database: str, callback: CallbackQuery, active=1):
    try:
        async with aiosqlite.connect(database) as conn:
            cursor = await conn.execute(f'SELECT word_len FROM sessions WHERE tg_id={callback.from_user.id} and active={active}')
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
            # тут ошибка, отбор + max attempt_number
            await conn.execute(f'UPDATE attempts SET chars_{field}="{letters}" WHERE session_id={session_id} AND attempt_number=(SELECT max(attempt_number) FROM attempts WHERE session_id={session_id})')
            await conn.commit()
    except aiosqlite.Error as e:
        print(e)


async def get_pos_letters(database, callback: CallbackQuery, with_callback=True, suf=None) -> str:
    try:
        if with_callback:
            suf, numlet = callback.data.split('_')
        if (suf == 'np' and numlet != 'agr') or (suf == 'add' and numlet == 'agr'):
            field = 'non_in_pos'
        else:
            field = 'in_pos'
        session_id = await get_active_session(database, callback)
        async with aiosqlite.connect(database) as conn:
            cursor = await conn.execute(f'SELECT chars_{field} FROM attempts WHERE session_id={session_id} AND attempt_number=(SELECT max(attempt_number) FROM attempts WHERE session_id={session_id})')
            res = await cursor.fetchone()
            return res[0]
    except aiosqlite.Error as e:
        print(e)
        return None


async def insert_positions_to_attempt(database: str, callback: CallbackQuery):
    try:
        suf, pl  = callback.data.split('_')
        if 'np' == suf:
            field = 'non_in_pos'
        else:
            field = 'in_pos'
        pos_letters = await get_pos_letters(database, callback)
        if pos_letters:
            pos_letters = pos_letters.split()
        else:
            pos_letters = []
        pos_letters.append(pl)
        # print(suf, pl, *pos_letters)
        session_id = await get_active_session(database, callback)
        # print(f'UPDATE attempts SET chars_{field}="{":".join(pos_letters)}" WHERE session_id={session_id} AND attempt_number=(SELECT max(attempt_number) FROM attempts WHERE session_id={session_id})')
        async with aiosqlite.connect(database) as conn:
            await conn.execute(f'UPDATE attempts SET chars_{field}="{":".join(pos_letters)}" WHERE session_id={session_id} AND attempt_number=(SELECT max(attempt_number) FROM attempts WHERE session_id={session_id})')
            await conn.commit()
    except aiosqlite.Error as e:
        print(e)


async def reset_positions_to_attempt(database: str, callback: CallbackQuery):
    try:
        suf, pl  = callback.data.split('_')
        if 'np' in callback.data:
            field = 'non_in_pos'
        else:
            field = 'in_pos'
        pos_letters = await get_pos_letters(database, callback)
        if pos_letters:
            pos_letters = pos_letters.split()
        else:
            pos_letters = []
        pos_letters.append(pl)
        session_id = await get_active_session(database, callback)
        # print(f'UPDATE attempts SET chars_{field}="{":".join(pos_letters)}" WHERE session_id={session_id} AND attempt_number=(SELECT max(attempt_number) FROM attempts WHERE session_id={session_id})')
        async with aiosqlite.connect(database) as conn:
            await conn.execute(f'UPDATE attempts SET chars_{field}="" WHERE session_id={session_id} AND attempt_number=(SELECT max(attempt_number) FROM attempts WHERE session_id={session_id})')
            await conn.commit()
    except aiosqlite.Error as e:
        print(e)


async def get_all_data_attempt(database: str, callback: CallbackQuery, passive=False):
    try:
        res = {}
        if passive:
            session_id = await get_active_session(database, callback, active=0)
            async with aiosqlite.connect(database) as conn:
                query = f'SELECT chars_excluded, chars_included, chars_non_in_pos, chars_in_pos FROM attempts WHERE session_id={session_id} AND attempt_number=(SELECT max(attempt_number) FROM attempts WHERE session_id={session_id})'
                cursor = await conn.execute(query)
                data = await cursor.fetchone()
                res['ex'] = data[0]
                res['in'] = data[1]
                res['np'] = data[2]
                res['ip'] = data[3]
            return res
        else:
            session_id = await get_active_session(database, callback)
            suf, cmd = callback.data.split('_')
            if (suf == 'ip' and cmd == 'agr') or (suf == 'next' and cmd == 'attempt') or (suf == 'add' and cmd == 'agr'):
                async with aiosqlite.connect(database) as conn:
                    query = f'SELECT chars_excluded, chars_included, chars_non_in_pos, chars_in_pos FROM attempts WHERE session_id={session_id} AND attempt_number=(SELECT max(attempt_number) FROM attempts WHERE session_id={session_id})'
                    cursor = await conn.execute(query)
                    data = await cursor.fetchone()
                    res['ex'] = data[0]
                    res['in'] = data[1]
                    res['np'] = data[2]
                    res['ip'] = data[3]
        return res
    except aiosqlite.Error as e:
        print(e)
        return False


async def get_words_from_dict(database: str, length: int):
    try:
        res_list = []
        query = f'SELECT word FROM dictionary WHERE length(word) = {length}'
        async with aiosqlite.connect(database) as conn:
            cursor = await conn.execute(query)
            result = await cursor.fetchall()
        for i in result:
            res_list.append(i[0])
        res_list.sort()
        return res_list
    except aiosqlite.Error as e:
        print(e)
        return False


async def get_words_from_filtered_dict(database: str, start: int, end: int, callback: CallbackQuery):
    try:
        session_id = await get_active_session(database, callback)
        res_list = []
        query = f'SELECT word FROM filtered_dicts WHERE session_id={session_id} limit {start},{end}'
        async with aiosqlite.connect(database) as conn:
            cursor = await conn.execute(query)
            result = await cursor.fetchall()
        for i in result:
            res_list.append(i[0])
        # res_list.sort()
        return res_list
    except aiosqlite.Error as e:
        print(e)
        return False


async def insert_filtered_dict(database: str, words: list, callback: CallbackQuery):
    try:
        session_id = await get_active_session(database, callback)
        async with aiosqlite.connect(database) as conn:
            for w in words:
                query = f'INSERT INTO filtered_dicts ("tg_id", "word", "session_id") VALUES ({callback.from_user.id}, "{w}", {session_id})'
                await conn.execute(query)
            await conn.commit()
    except aiosqlite.Error as e:
        print(e)
        return False


async def count_filtered_words(database: str, callback: CallbackQuery):
    try:
        session_id = await get_active_session(database, callback)
        query = f'SELECT count() FROM filtered_dicts WHERE tg_id={callback.from_user.id} AND session_id={session_id}'
        async with aiosqlite.connect(database) as conn:
            cursor = await conn.execute(query)
            result = await cursor.fetchone()
        return result[0]
    except aiosqlite.Error as e:
        print(e)
        return False


async def end_session(database: str, callback: CallbackQuery):
    try:
        session_id = await get_active_session(database, callback)
        query = f'UPDATE sessions SET ended=datetime("now"), active=0 WHERE id={session_id} AND tg_id={callback.from_user.id}'
        async with aiosqlite.connect(database) as conn:
            await conn.execute(query)
            await conn.commit()
        return True
    except aiosqlite.Error as e:
        print(e)
        return False


async def get_random_word(database: str, callback: CallbackQuery, lenght):
    try:
        query = f'SELECT word FROM dictionary WHERE length(word)={lenght} ORDER BY random() LIMIT 1;'
        async with aiosqlite.connect(database) as conn:
            cursor = await conn.execute(query)
            res = await cursor.fetchone()
        return res[0]
    except aiosqlite.Error as e:
        print(e)
        return False


async def get_time_from_last(database: str, callback: CallbackQuery|Message):
    try:
        query = f'SELECT (julianday("now") - julianday(activity)) * 86400 FROM users WHERE tg_id={callback.from_user.id}'
        async with aiosqlite.connect(database) as conn:
            cursor = await conn.execute(query)
            res = await cursor.fetchone()
        return res[0]
    except aiosqlite.Error as e:
        print(e)
        return False       


async def get_len_and_status(database: str, message: Message):
    query = f'SELECT active, word_len, result FROM sessions WHERE tg_id={message.from_user.id} ORDER BY id DESC LIMIT 1'
    try:
        async with aiosqlite.connect(database) as conn:
            cursor = await conn.execute(query)
            res = await cursor.fetchone()
        return res
    except aiosqlite.Error as e:
        print(e)
        return False


async def insert_session_word(database: str, message: Message):
    '''
    Функция добавляет слово которое было подобрано пользователем
    '''
    try:
        session_id = await get_active_session(database, message, active=0)
        async with aiosqlite.connect(database) as conn:
            await conn.execute(f'UPDATE sessions SET result="{message.text}" WHERE id={session_id} AND tg_id={message.from_user.id}')
            await conn.commit()
    except Error:
        print(Error)
