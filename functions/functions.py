import re
from itertools import repeat


from pprint import pprint

def show_pos_letters(line: str) -> str:
    '''
    Функция формирует строку из позиций и букв стоящих на указанных позициях
    '''
    if not line:
        return ''
    res = {}
    out_line = '\n'
    for i in line.split(':'):
        if i[0] not in res:
            res[i[0]] = {i[1]}
        else:
            res[i[0]].add(i[1])
    for k in sorted(res.keys()):
        out_line += f'{k} - {",".join(res[k])}\n'
    return out_line


def filter_regex(line, regex) -> bool:
    '''
    Функция ищет совпадение по регулярному выражению
    '''
    if re.match(regex, line):
        return True
    else:
        return False


def words_filter(dictionary: list, params: dict) -> list:
    '''
    Функция фильтрации слов по параметрам
    '''
    def include_filter(word: str, line_letters: str) -> bool:
        for i in line_letters:
            if i not in word:
                return False
        return True

    for i in params:
        if i in ['ex', 'np', 'ip']:
            dictionary = list(filter(lambda x: filter_regex(x, params[i]), dictionary))
        elif i == 'in':
            dictionary = list(filter(lambda x: include_filter(x, params[i]), dictionary))
    dictionary.sort()
    return dictionary


def set_exclude_regex(line: str) -> str:
    '''
    Функция формирует регулярку для исключаемых букв
    '''
    if line:
        head_line = '^((?!['
        tail_line = '])\w)*$'
        return f'{head_line}{line}{tail_line}'
    else:
        return False


def set_include(line: str) -> str:
    '''
    Функция формирует регулярку для входящих букв
    '''
    if line:
        # head_line = '^\w*['
        # tail_line = ']{1}\w*$'
        # return f'{head_line}{line}{tail_line}'
        return line
    else:
        return False


def set_position_dict(line: str) -> dict:
    res = {}
    if not line:
        return {}
    for i in line.split(':'):
        if int(i[0]) in res:
            res[int(i[0])].append(i[1])
        else:
            res[int(i[0])] = [i[1]]
    return res


def set_np_regex(line: str, length: int):
    '''
    Функция формирует регулярку для букв находящихся не на своих позициях
    '''
    res = []
    empty_letter = '\w'
    positons = set_position_dict(line)
    head_line='[^'
    tail_line=']'
    for i in range(1, length + 1):
        if i in positons:
            res.append(f'{head_line}{"".join(positons[i])}{tail_line}')
        else:
            res.append(empty_letter)
    return ''.join(res)


def set_ip_regex(line: str, length: int):
    '''
    Функция формирует регулярку для букв находящихся не на своих позициях
    '''
    res = []
    empty_letter = '\w'
    positons = set_position_dict(line)
    head_line='['
    tail_line=']'
    for i in range(1, length + 1):
        if i in positons:
            res.append(f'{head_line}{"".join(positons[i])}{tail_line}')
        else:
            res.append(empty_letter)
    return ''.join(res)


def gen_params(exc_line: str, inc_line: str, np_line: str, ip_line: str, length: int) -> list:
    params = {}
    if line:=set_exclude_regex(exc_line):
        params['ex'] = line
    if line:=set_include(inc_line):
        params['in'] = line
    if line:=set_np_regex(np_line, length):
        params['np'] = line
    if line:=set_ip_regex(ip_line, length):
        params['ip'] = line
    return params


def show_words(words: dict[str], cols: int) -> str:
    c = -1
    res = []
    mid_res = []
    for word in words:
        if c <= cols:
            c += 1
            mid_res.append(word)
        else:
            c = 0
            res.append('  '.join(mid_res))
            mid_res = [word]
    if mid_res:
        res.append(' '.join(mid_res))
    return '\n'.join(res)



if __name__ == '__main__':

    words = [
        'ррарр',
        'рррра',
        'арррр',
        'ясное',
        'ясной',
        'ясном',
        'ясною',
        'ясную',
        'ясные',
        'ясный',
        'ясным',
        'ясных',
        'яспис',
        'яссах',
        'яства',
        'ястве',
        'яство',
        'яству',
        'ястык',
        'ясырь',
        'ятвяг',
        'ятках',
        'яткой',
        'яткою',
        'ятных',
        'ятовь',
        'яться',
        'ятями',
        'яффой',
        'яхонт',
        'яхтам',
        'яхтах',
        'яхтой',
        'яхтою',
        'ячать',
        'ячеей',
        'ячеек',
        'ячеею',
        'ячеям',
        'ячеях',
        'ячеёй',
        'ячеёю',
        'ячная',
        'ячное',
        'ячной',
        'ячном',
        'ячною',
        'ячную',
        'ячные',
        'ячный',
        'ячным',
        'ячных',
        'ячьей',
        'ячьем',
        'ячьим',
        'ячьих',
        'яшмой',
        'яшмою',
        'ящера',
        'ящере',
        'ящеру',
        'ящеры',
        'ящика',
        'ящике',
        'ящики',
        'ящику',
        'ящура',
        'ящуре',
        'ящуру',
        'ёжась',
        'ёжика',
        'ёжике',
        'ёжики',
        'ёжику',
        'ёжила',
        'ёжили',
        'ёжило',
        'ёжите',
        'ёжить',
        'ёжишь',
        'ёжусь',
        'ёжься',
        'ёжьте',
        'ёкаем',
        'ёкает',
        'ёкала',
        'ёкали',
        'ёкало',
        'ёкать',
        'ёкают',
        'ёкнем',
        'ёкнет',
        'ёкнув',
        'ёкнул',
        'ёкнут',
        'ёлкам',
        'ёлках',
        'ёлкой',
        'ёлкою',
        'ёмкая',
        'ёмкие',
        'ёмкий',
        'ёмким',
        'ёмких',
        'ёмкое',
        'ёмкой',
        'ёмком',
        'ёмкою',
        'ёмкую',
        'ёрзай',
        'ёрзал',
        'ёрзаю',
        'ёрзая',
        'ёрник',]


    print(show_words(words, 3))
