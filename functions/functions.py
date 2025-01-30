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


# if __name__ == '__main__':
#     show_pos_letters('5у:5п:3п:5у:5п:4у')