import re


def filter_regex(line, regex) -> bool:
    if re.match(regex, line):
        return True
    else:
        return False


'''
OUT : ^((?![а])\w)*$
IN : ^\w*[а]{1}\w*$



'''

if __name__ == '__main__':
    m = re.match(r'^((?![а])\w)*$', 'ячнея')
    # print(filter_regex(, ))
    print(m)

