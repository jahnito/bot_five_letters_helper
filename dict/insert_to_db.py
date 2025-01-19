import sqlite3


src = 'dict/russian.txt'
dst = 'database.db'


with open(src, 'r') as f, sqlite3.connect(dst) as conn:
    for i in f:
        conn.execute(f'INSERT INTO dictionary (word, added, changed) VALUES ("{i.strip()}", datetime("now"), datetime("now"))')
    conn.commit()


'''
INSERT INTO dictionary (word, added, changed) VALUES ('123', datetime('now'), datetime('now'))
'''