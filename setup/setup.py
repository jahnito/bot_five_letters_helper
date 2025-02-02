import sqlite3
import pathlib


SETUP_PATH = pathlib.Path(__file__).parent.parent
DB_PATH = pathlib.Path(str(SETUP_PATH) + '/database.db')
DB_SCRIPT = pathlib.Path(str(SETUP_PATH) + '/database.sql')


if DB_PATH.exists():
    print(f'Файл базы данных существует\n{DB_PATH}')
else:
    try:
        scr = open(DB_SCRIPT, 'r')
        with sqlite3.connect(DB_PATH) as conn:
            conn.executescript(scr.read())
            conn.commit()        
        scr.close()
    except sqlite3.Error as e:
        print(e)
