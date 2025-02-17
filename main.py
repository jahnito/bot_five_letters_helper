from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from aiogram.types import Message, ChatMemberUpdated, CallbackQuery
from aiogram import F
from pprint import pprint
from config import Config
from db import *
from filters import *
from functions import show_pos_letters, gen_params, words_filter, show_words
from lexicon import RU
from kb import *


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


### start master find word ###


@dp.message(Command(commands=['guess']))
async def process_run_guess(message: Message):
    await update_activity_user(_db, message)
    if await check_active_session(_db, message):
        await message.answer(text='Сессия бодбора слов запущена')
    else:
        await message.answer(
            text=RU['kb_choice_length'],
            reply_markup=gen_kb_set_lenght(),
            )


@dp.callback_query(IsGetLengthWord())
async def process_create_session(callback: CallbackQuery):
    await update_activity_user(_db, callback.message)
    if await check_active_session(_db, callback):
        print('Сессия запущена')
    else:
        await create_session(_db, callback) # создаем сессию
        await create_attempt(_db, callback) # создаем первую попытку
        await callback.message.edit_text(
            text=RU['kb_exc_0'],
            reply_markup=gen_kb_letters('rem')
            )


@dp.callback_query(IsNextAttempt())
async def process_create_next_attempt(callback: CallbackQuery):
    await update_activity_user(_db, callback.message)
    data_prev_att = await get_all_data_attempt(_db, callback)
    await create_attempt_next(_db, callback, data_prev_att)
    await delete_filtered_dict(_db, callback)

    chars_excluded = await get_letters(_db, callback)
    await callback.message.edit_text(
        RU['kb_exc_head'] +
        f'{", ".join(sorted(chars_excluded))}' +
        RU['kb_exc_footer'],
        reply_markup=gen_kb_letters('rem'))


@dp.callback_query(IsRemButton())
async def get_excluded_letter(callback: CallbackQuery, let):
    '''
    Ловим исключаемые буквы с инлайн клавиатуры
    '''
    chars_excluded = await get_letters(_db, callback)
    chars_included = await get_letters_included(_db, callback)
    await update_activity_user(_db, callback.message)
    if chars_included and let in chars_included:
        await callback.answer(f'Буква *{let}* во входящих')
    else:
        if chars_excluded:
            # Повтороный выбор буквы
            if let in chars_excluded:
                await callback.answer(f'Буква *{let}* уже была исключена')
                letters = chars_excluded
                await callback.message.edit_text(
                    RU['kb_exc_head'] +
                    f'{", ".join(letters)}' +
                    RU['kb_exc_footer'],
                    reply_markup=callback.message.reply_markup)
            # Первичный выбор буквы
            else:
                await callback.answer(f'Для исключения выбрана буква *{let}*')
                letters = chars_excluded + let
        else:
            letters = let
        await insert_chars_to_attempt(_db, callback, letters)
        await callback.message.edit_text(
            RU['kb_exc_head'] +
            f'{", ".join(sorted(letters))}' +
            RU['kb_exc_footer'],
            reply_markup=callback.message.reply_markup)


@dp.callback_query(IsCncRemButton())
async def cancel_last_rem_letter(callback: CallbackQuery):
    '''
    Удаляем последнюю исключаемую букву
    '''
    chars_excluded = await get_letters(_db, callback)
    await update_activity_user(_db, callback.message)
    if chars_excluded:
        await callback.answer(f'Возвращена буква *{chars_excluded[-1]}*')
        await insert_chars_to_attempt(_db, callback, chars_excluded[:-1])
        await callback.message.edit_text(
            RU['kb_exc_head'] +
            f'{", ".join(sorted(chars_excluded[:-1]))}' +
            RU['kb_exc_footer'],
            reply_markup=callback.message.reply_markup)
    else:
        await callback.answer(f'Список букв пуст')


@dp.callback_query(IsRstRemButton())
async def reset_last_rem_letter(callback: CallbackQuery):
    '''
    Очищаем список букв
    '''
    await update_activity_user(_db, callback.message)
    chars_excluded = await get_letters(_db, callback)
    if chars_excluded:
        await callback.answer(f'Список букв очищен!')
        await insert_chars_to_attempt(_db, callback, '')
        await callback.message.edit_text(
            RU['kb_exc_head'] +
            RU['kb_exc_footer'],
            reply_markup=callback.message.reply_markup)
    else:
        await callback.answer(f'Список букв пуст')


@dp.callback_query(IsAgrRemButton())
async def agree_excluded_letters(callback: CallbackQuery):
    cur_attempt = await get_current_attempt(_db, callback)
    await update_activity_user(_db, callback.message)
    # Если это не первая попытка, выводим клаву с уже существующими буквами
    print(cur_attempt)
    if cur_attempt > 1:
        chars_included = await get_letters(_db, callback)
        await callback.message.edit_text(
            text=f'✳️ Буквы присутствующие в слове: {", ".join(sorted(chars_included))}'
            '\n\nдля продолжения нажмите Принять',
            reply_markup=gen_kb_letters('add')
        )
    else:
        await callback.message.edit_text(
            text=f'✳️ Выберите буквы которые есть в слове'
                '\n\nвыбери буквы которые есть в слове и нажми Принять',
            reply_markup=gen_kb_letters('add')
            )


@dp.callback_query(IsAddButton())
async def get_included_letter(callback: CallbackQuery, let):
    chars_included = await get_letters(_db, callback)
    chars_excluded = await get_letters_excluded(_db, callback)
    length = await get_length_word(_db, callback)
    await update_activity_user(_db, callback.message)
    if chars_excluded and let in chars_excluded:
        # Проверка вхождения буквы в исключенных
        await callback.answer(f'Буква *{let}* в исключениях')
    elif chars_included and length == len(chars_included):
        await callback.answer('Количество букв превышает количество букв в слове')
    else:
        if chars_included:
            if let in chars_included:
                await callback.answer(f'Буква *{let}* уже добавлена')
                letters = chars_included
            else:
                letters = chars_included + let
                await callback.answer(f'Добавлена буква *{let}*')
        else:
            letters = let
        await insert_chars_to_attempt(_db, callback, letters)
        await callback.message.edit_text(
            f'✳️ Буквы присутствующие в слове: {", ".join(sorted(letters))}'
            '\n\nдля продолжения нажмите Принять',
            reply_markup=callback.message.reply_markup)


@dp.callback_query(IsCncAddButton())
async def cancel_last_add_letter(callback: CallbackQuery):
    '''
    Удаляем последнюю добавленную букву
    '''
    await update_activity_user(_db, callback.message)
    chars_included = await get_letters(_db, callback)
    if chars_included:
        await callback.answer(f'Возвращена буква *{chars_included[-1]}*')
        await insert_chars_to_attempt(_db, callback, chars_included[:-1])
        await callback.message.edit_text(
            f'✳️ Буквы присутствующие в слове: {", ".join(sorted(chars_included[:-1]))}'
            '\n\nдля продолжения нажмите Принять',
            reply_markup=callback.message.reply_markup)
    else:
        await callback.answer(f'Список букв пуст')


@dp.callback_query(IsRstAddButton())
async def reset_last_add_letter(callback: CallbackQuery):
    '''
    Очищаем список добавленных букв
    '''
    await update_activity_user(_db, callback.message)
    chars_included = await get_letters(_db, callback)
    if chars_included:
        await callback.answer(f'Список букв очищен!')
        await insert_chars_to_attempt(_db, callback, '')
        await callback.message.edit_text(
            '✳️ Буквы присутствующие в слове: '
            '\n\nдля продолжения нажмите Принять',
            reply_markup=callback.message.reply_markup)
    else:
        await callback.answer(f'Список букв пуст')


@dp.callback_query(IsAgrAddButton())
async def agree_included_letters(callback: CallbackQuery):
    await update_activity_user(_db, callback.message)
    chars_included = await get_letters(_db, callback)
    cur_attempt = await get_current_attempt(_db, callback)
    # Если это не первая попытка, выводим клаву с уже существующими буквами
    if cur_attempt > 0:
        letters = await get_pos_letters(_db, callback)
        pos_letters = show_pos_letters(letters)
        await callback.message.edit_text(
            text='📌 Буквы не на своих местах\n'
                f'{pos_letters}',
            reply_markup=gen_kb_letters_in(chars_included, 'np')
        )
    else:
        await callback.message.edit_text(
            text='🚫 Выберите букву, для которой известно место где этой'
                'буквы нет\n\nчтобы продолжить/пропустить: нажмите Принять',
            # np = non-position
            reply_markup=gen_kb_letters_in(chars_included, 'np')
            )


@dp.callback_query(IsNonposLetterButton())
async def press_nonpos_button(callback: CallbackQuery, let):
    length = await get_length_word(_db, callback)
    await update_activity_user(_db, callback.message)
    await callback.message.edit_text(
        text=f'📌 Выбери позицию где нет буквы {let}',
        reply_markup=gen_kb_line(length, 'np', let)
    )


@dp.callback_query(IsNonposNumberButton())
async def press_nonpos_num_button(callback: CallbackQuery):
    chars_included = await get_letters(_db, callback)
    letters = await get_pos_letters(_db, callback)
    pos_letters = show_pos_letters(letters)
    await update_activity_user(_db, callback.message)
    if letters and callback.data.split('_')[-1] in letters.split(':'):
        await callback.answer(text='Эта буква уже добавлена в этой позиции')
        await callback.message.edit_text(
            text='📌 Буквы не на своих местах\n'
                f'{pos_letters}',
            reply_markup=gen_kb_letters_in(chars_included, 'np')
        )
    else:
        await insert_positions_to_attempt(_db, callback)    
        letters = await get_pos_letters(_db, callback)
        pos_letters = show_pos_letters(letters)
        await callback.message.edit_text(
            text='📌 Буквы не на своих местах\n'
                f'{pos_letters}',
            reply_markup=gen_kb_letters_in(chars_included, 'np')
        )


@dp.callback_query(IsRstNposButton())
async def press_nonpos_rst_button(callback: CallbackQuery):
    await update_activity_user(_db, callback.message)
    await reset_positions_to_attempt(_db, callback)
    chars_included = await get_letters(_db, callback)
    await callback.message.edit_text(
        text='📌 Буквы не на своих местах\n\n',
        # np = non-position
        reply_markup=gen_kb_letters_in(chars_included, 'np')
        )


@dp.callback_query(IsAgrNposButton())
async def agree_nonpos_letters(callback: CallbackQuery):
    chars_included = await get_letters(_db, callback)
    cur_attempt = await get_current_attempt(_db, callback)
    await update_activity_user(_db, callback.message)
    # Если это не первая попытка, выводим клаву с уже существующими буквами
    if cur_attempt > 0:
        letters = await get_pos_letters(_db, callback)
        pos_letters = show_pos_letters(letters)
        await callback.message.edit_text(
            text='📌 Выбираем букву, для которой известна позиция\n'
                f'{pos_letters}',
            reply_markup=gen_kb_letters_in(chars_included, 'ip')
        )
    else:
        await callback.message.edit_text(
            text='📌 Выбираем букву, для которой известна позиция\n',
            # ip = in-position
            reply_markup=gen_kb_letters_in(chars_included, 'ip')
        )


@dp.callback_query(IsPosLetterButton())
async def press_pos_button(callback: CallbackQuery, let):
    length = await get_length_word(_db, callback)
    await update_activity_user(_db, callback.message)
    await callback.message.edit_text(
        text=f'📌 Выбери позицию буквы {let}',
        reply_markup=gen_kb_line(length, 'ip', let)
    )


@dp.callback_query(IsPosNumberButton())
async def press_pos_num_button(callback: CallbackQuery):
    chars_included = await get_letters(_db, callback)
    letters = await get_pos_letters(_db, callback)
    pos_letters = show_pos_letters(letters)
    await update_activity_user(_db, callback.message)
    # non_letters = await get_pos_letters(_db, callback, with_callback=False, suf='np')
    non_letters = await get_pos_letters(_db, callback)

    if letters and callback.data.split('_')[-1] in letters.split(':'):
        await callback.answer(text='Эта буква уже добавлена в этой позиции')
        await callback.message.edit_text(
            text='📌 Выбираем букву, для которой известна позиция\n'
                f'{pos_letters}',
            reply_markup=gen_kb_letters_in(chars_included, 'ip')
        )
    elif non_letters and callback.data.split('_')[-1] in non_letters:
        await callback.answer(text='Эта буква уже не в соответсвующей позиции')
        await callback.message.edit_text(
            text='📌 Выбираем букву, для которой известна позиция\n'
                f'{pos_letters}',
            reply_markup=gen_kb_letters_in(chars_included, 'ip')
        )
    else:
        await insert_positions_to_attempt(_db, callback)    
        letters = await get_pos_letters(_db, callback)
        pos_letters = show_pos_letters(letters)
        await callback.message.edit_text(
            text='📌 Выбираем букву, для которой известна позиция\n'
                f'{pos_letters}',
            reply_markup=gen_kb_letters_in(chars_included, 'ip')
        )


@dp.callback_query(IsRstPosButton())
async def press_pos_rst_button(callback: CallbackQuery):
    await reset_positions_to_attempt(_db, callback)
    await update_activity_user(_db, callback.message)
    chars_included = await get_letters(_db, callback)
    await callback.message.edit_text(
        text='📌 Выбираем букву, для которой известна позиция\n\n',
        # ip = in-position
        reply_markup=gen_kb_letters_in(chars_included, 'ip')
        )


@dp.callback_query(IsAgrPosButton())
async def agree_pos_letters(callback: CallbackQuery):
    await update_activity_user(_db, callback.message)
    # Длина слова
    length = await get_length_word(_db, callback)
    # Берем все строки из попытки
    data = await get_all_data_attempt(_db, callback)
    # Выбираем все слова из словаря определенной длины
    dictionary = await get_words_from_dict(_db, length)
    # Формируем словарь параметров с регулярками
    params = gen_params(data.get('ex', ''), data.get('in', ''), data.get('np', ''), data.get('ip', ''), length)
    # Фильтруем словарь, только подходящие слова
    dictionary = words_filter(dictionary, params)
    # В БД заносим отфильтрованный список слов
    await insert_filtered_dict(_db, dictionary, callback)
    length_filtered = len(dictionary)
    pages = length_filtered // 40
    words = await get_words_from_filtered_dict(_db, 0, 40, callback)
    text = show_words(words, 3)
    await callback.message.edit_text(
        text=text,
        reply_markup=gen_kb_words(3, 'words', 2, f'{1}/{pages + 1}({len(dictionary)})',)
    )


@dp.callback_query(IsNextButton())
async def press_next_button(callback: CallbackQuery, nxt: int):
    await update_activity_user(_db, callback.message)
    num_words = await count_filtered_words(_db, callback)
    words = await get_words_from_filtered_dict(_db, (nxt - 1) * 40, 40, callback)
    pages = num_words // 40 + 1
    if pages == nxt:
        next_page = nxt
    else:
        next_page = nxt + 1
    text = show_words(words, 3)
    await callback.message.edit_text(
        text=text,
        reply_markup=gen_kb_words(3, 'words', next_page, f'{nxt}/{pages}({num_words})',)
    )


@dp.callback_query(IsPrevButton())
async def press_prev_button(callback: CallbackQuery, prv: int):
    await update_activity_user(_db, callback.message)
    num_words = await count_filtered_words(_db, callback)
    words = await get_words_from_filtered_dict(_db, (prv - 1) * 40, 40, callback)
    pages = num_words // 40 + 1
    if prv > 1:
        prev_page = prv - 1
    else:
        prev_page = prv
    text = show_words(words, 3)
    await callback.message.edit_text(
        text=text,
        reply_markup=gen_kb_words(3, 'words', prev_page, f'{prv}/{pages}({num_words})',)
    )


@dp.callback_query(IsAttemptEnd())
async def press_agr_attempt(callback: CallbackQuery, page):
    await update_activity_user(_db, callback.message)
    await callback.message.edit_text(
        text='Подбор слов завершен',
        reply_markup=gen_kb_end_attempt(page)
    )
    # print(page)


@dp.callback_query(IsFindedWord())
async def press_word_find(callback: CallbackQuery):
    await update_activity_user(_db, callback.message)
    await end_session(_db, callback)
    await delete_filtered_dict(_db, callback)
    await callback.message.edit_text(
        text='Если я вам помог, то напишите какое слово подошло.'
    )

### end master find word ###

### start random offer word ###

@dp.message(Command(commands=['random']))
async def process_run_random_word(message: Message):
    await update_activity_user(_db, message)
    await message.answer(
        text=RU['kb_choice_length'],
        reply_markup=gen_kb_set_lenght(suf='R'),
        )


@dp.callback_query(IsGetLengthRandomWord())
async def press_word_find(callback: CallbackQuery, length: int):
    await update_activity_user(_db, callback.message)
    word = await get_random_word(_db, callback, length)
    await callback.message.edit_text(text=word)



@dp.callback_query()
async def any_callback(callback: CallbackQuery):
    await update_activity_user(_db, callback.message)
    print(callback.data)


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await update_activity_user(_db, message)
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
