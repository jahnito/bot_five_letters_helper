import sqlite3

def check_exist_user(database, id):
    try:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute(f'SELECT tg_id FROM users WHERE tg_id={id}')
        if cursor.fetchone():
            print('YES')
        else:
            print('NO')
    except sqlite3.Error as e:
        print(e)


if __name__ == '__main__':
    check_exist_user('database.db', 1737180589)
