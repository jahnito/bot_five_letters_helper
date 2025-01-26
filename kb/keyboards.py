from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


ABC = [chr(i) for i in range(1072, 1104)] # + [chr(1105)]


def gen_kb_set_lenght():
    builder = InlineKeyboardBuilder()
    builder.add(*[InlineKeyboardButton(text=str(i), callback_data=f'length_{str(i)}') for i in range(4, 7)])
    return builder.as_markup()


def gen_kb_letters(suffix: str) -> InlineKeyboardMarkup:
    '''
    Клавиатура с алфавитом
    '''
    builder = InlineKeyboardBuilder()
    builder.add(*[InlineKeyboardButton(text=i, callback_data=f'{suffix}_{i}') for i in ABC ])
    rst_btn = InlineKeyboardButton(text='❌ Сброс', callback_data=f'{suffix}_rst')
    cnc_btn = InlineKeyboardButton(text='⭕️ Отмена', callback_data=f'{suffix}_cnc')
    agr_btn = InlineKeyboardButton(text='✅ Принять', callback_data=f'{suffix}_agr')
    builder.add(rst_btn, cnc_btn, agr_btn)
    builder.adjust(8, repeat=True)
    return builder.as_markup()


def gen_kb_letters_in(letters: str, suffix: str):
    builder = InlineKeyboardBuilder()
    builder.add(*[InlineKeyboardButton(text=i, callback_data=f'{suffix}_{i}') for i in letters])
    rst_btn = InlineKeyboardButton(text='❌ Сброс', callback_data=f'{suffix}_rst')
    cnc_btn = InlineKeyboardButton(text='⭕️ Отмена', callback_data=f'{suffix}_cnc')
    agr_btn = InlineKeyboardButton(text='✅ Принять', callback_data=f'{suffix}_agr')
    builder.add(rst_btn, cnc_btn, agr_btn)
    builder.adjust(len(letters))
    return builder.as_markup()


def gen_kb_line(lenght: int, suffix: str, let: str) -> InlineKeyboardMarkup:
    '''
    Клавиатура с позициями слова
    '''
    builder = InlineKeyboardBuilder()
    builder.add(*[InlineKeyboardButton(text=str(i), callback_data=f'{suffix}_{str(i)+let}') for i in range(1, lenght + 1)])
    cnc_btn = InlineKeyboardButton(text='⭕️ Отмена', callback_data=f'{suffix}_cnc')
    # builder.adjust(8)
    builder.add(cnc_btn)
    builder.adjust(lenght)
    return builder.as_markup()
