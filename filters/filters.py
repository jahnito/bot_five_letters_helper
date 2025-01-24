from aiogram.filters import BaseFilter
from aiogram import F
from aiogram.types import CallbackQuery


__all__ = ['IsRemoveLetter']


class IsRemoveLetter(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, let = callback.data.split('_')
            if suf == 'rem' and len(let) == 1:
                return {'let': let}
            else:
                return False
        except (ValueError, IndexError) as e:
            return False 
