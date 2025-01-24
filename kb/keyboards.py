from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


ABC = [chr(i) for i in range(1072, 1104)] # + [chr(1105)]


def gen_kb_letters(suffix: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(*[ InlineKeyboardButton(text=i, callback_data=f'{suffix}_{i}') for i in ABC ])
    rst_btn = InlineKeyboardButton(text='❌ Сброс', callback_data=f'{suffix}_rst')
    cnc_btn = InlineKeyboardButton(text='⭕️ Отмена', callback_data=f'{suffix}_cnc')
    agr_btn = InlineKeyboardButton(text='✅ Принять', callback_data=f'{suffix}_agr')
    builder.add(rst_btn, cnc_btn, agr_btn)
    builder.adjust(8, repeat=True)
    return builder.as_markup()
