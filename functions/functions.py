import re
from itertools import repeat


def show_pos_letters(line: str) -> str:
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
    if re.match(regex, line):
        return True
    else:
        return False


def words_filter(dictionary: list, params: dict) -> list:
    for i in params:
        dictionary = list(filter(lambda x: filter_regex(x, params[i]), dictionary))
        # dictionary = list(filter(filter_regex, zip(dictionary, repeat(params[i]))))
        # print(params[i])
    # print(dictionary)
    dictionary.sort()
    return dictionary


    # dictionary = filter(filter_regex, zip(dictionary, repeat()))


if __name__ == '__main__':
    params = {
              'ex': '^[^ёЁ]+$',
            #   'in': '[а]+',
            #   'np': '',
            #   'ip': ''
              }


    words = ['ясное',
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

    words.sort()


    # print(*words, sep='\n')

    print(*words)


    print('\n\n')

    print(*words_filter(words, params))
