from aiogram.filters import BaseFilter
from aiogram import F
from aiogram.types import CallbackQuery


__all__ = ['IsRemButton', 'IsCncRemButton', 'IsRstRemButton', 'IsAgrRemButton',
           'IsAddButton', 'IsCncAddButton', 'IsRstAddButton', 'IsAgrAddButton',
           'IsNonposLetterButton', 'IsNonposNumberButton', 'IsGetLengthWord',
           'IsRstNposButton', 'IsAgrNposButton', 'IsPosLetterButton',
           'IsPosNumberButton', 'IsAgrPosButton', 'IsRstPosButton',
           'IsPrevButton', 'IsNextButton', 'IsAttemptEnd', 'IsFindedWord',
           'IsNextAttempt', 'IsGetLengthRandomWord'
           ]


# start find word

class IsGetLengthWord(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, num = callback.data.split('_')
            if suf == 'length' and num.isdigit():
                return {'length': int(num)}
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False


class IsRemButton(BaseFilter):
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


class IsCncRemButton(BaseFilter):
    '''
    Фильтр отлова колбэка по нажатию кнопки Отмена
    '''
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, cmd = callback.data.split('_')
            if suf == 'rem' and cmd == 'cnc':
                return True
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False


class IsRstRemButton(BaseFilter):
    '''
    Фильтр отлова колбэка по нажатию кнопки Отмена
    '''
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, cmd = callback.data.split('_')
            if suf == 'rem' and cmd == 'rst':
                return True
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False


class IsAgrRemButton(BaseFilter):
    '''
    Фильтр отлова колбэка по нажатию Принять
    '''
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, cmd = callback.data.split('_')
            if suf == 'rem' and cmd == 'agr':
                return True
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False


class IsAddButton(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, let = callback.data.split('_')
            if suf == 'add' and len(let) == 1:
                return {'let': let}
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False


class IsCncAddButton(BaseFilter):
    '''
    Фильтр отлова колбэка по нажатию кнопки Отмена
    '''
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, cmd = callback.data.split('_')
            if suf == 'add' and cmd == 'cnc':
                return True
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False


class IsRstAddButton(BaseFilter):
    '''
    Фильтр отлова колбэка по нажатию кнопки Отмена
    '''
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, cmd = callback.data.split('_')
            if suf == 'add' and cmd == 'rst':
                return True
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False


class IsAgrAddButton(BaseFilter):
    '''
    Фильтр отлова колбэка по нажатию Принять
    '''
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, cmd = callback.data.split('_')
            if suf == 'add' and cmd == 'agr':
                return True
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False


class IsNonposLetterButton(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, let = callback.data.split('_')
            if suf == 'np' and let.isalpha() and len(let) == 1:
                return {'let': let}
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False


class IsNonposNumberButton(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, numlet = callback.data.split('_')
            if suf == 'np' and numlet[0].isdigit() and numlet[1].isalpha() and len(numlet) == 2:
                return True
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False


class IsRstNposButton(BaseFilter):
    '''
    Фильтр отлова колбэка по нажатию кнопки сброс
    '''
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, cmd = callback.data.split('_')
            if suf == 'np' and cmd == 'rst':
                return True
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False


class IsAgrNposButton(BaseFilter):
    '''
    Фильтр отлова колбэка по нажатию кнопки Принять
    '''
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, cmd = callback.data.split('_')
            if suf == 'np' and cmd == 'agr':
                return True
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False


class IsPosLetterButton(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, let = callback.data.split('_')
            if suf == 'ip' and let.isalpha() and len(let) == 1:
                return {'let': let}
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False


class IsPosNumberButton(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, numlet = callback.data.split('_')
            if suf == 'ip' and numlet[0].isdigit() and numlet[1].isalpha() and len(numlet) == 2:
                return True
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False


class IsAgrPosButton(BaseFilter):
    '''
    Фильтр отлова колбэка по нажатию кнопки Принять
    '''
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, cmd = callback.data.split('_')
            if suf == 'ip' and cmd == 'agr':
                return True
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False


class IsRstPosButton(BaseFilter):
    '''
    Фильтр отлова колбэка по нажатию кнопки сброс
    '''
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, cmd = callback.data.split('_')
            if suf == 'ip' and cmd == 'rst':
                return True
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False


class IsNextButton(BaseFilter):
    '''
    Фильтр отлова колбэка по нажатию кнопки следующй страницы
    '''
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, page = callback.data.split('_')
            if suf == 'nextW' and page.isdigit():
                return {'nxt': int(page)}
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False


class IsPrevButton(BaseFilter):
    '''
    Фильтр отлова колбэка по нажатию кнопки предыдущей страницы
    '''
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, page = callback.data.split('_')
            if suf == 'prevW' and page.isdigit():
                return {'prv': int(page)}
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False


class IsAttemptEnd(BaseFilter):
    '''
    Отлов нажатия кнопки принять после пролистывания перечня слов
    '''
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, num = callback.data.split('_')
            if suf == 'words' and num.isdigit():
                return {'page': num}
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False


class IsFindedWord(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, glag = callback.data.split('_')
            if suf == 'word' and glag == 'find':
                return True
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False


class IsNextAttempt(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, glag = callback.data.split('_')
            if suf == 'next' and glag == 'attempt':
                return True
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False


# start random word #

class IsGetLengthRandomWord(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, num = callback.data.split('_')
            if suf == 'lengthR' and num.isdigit():
                return {'length': int(num)}
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False
