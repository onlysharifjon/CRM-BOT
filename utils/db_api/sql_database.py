import sqlite3

connect = sqlite3.connect('crm_database.db')
cursor = connect.cursor()


def check_user(user_id):
    cursor.execute('CREATE TABLE IF NOT EXISTS users_table(user_id INTEGER UNIQUE,first_name TEXT)')

    tekshiruvchi = cursor.execute("SELECT * FROM users_table WHERE user_id=?", (user_id,)).fetchone()
    return tekshiruvchi


def register_user(user_id, full_name):
    try:
        cursor.execute('INSERT INTO users_table(user_id,first_name) VALUES(?,?)', (user_id, full_name))
        connect.commit()
        return 'Ro`yxatdan o`tildi'
    except:
        return 'Qandaydir Xatolik'


def change_name(user_id, full_name):
    try:
        cursor.execute('UPDATE users_table SET first_name=? WHERE user_id=?', (full_name, user_id))
        connect.commit()
        return f'Ismingiz {full_name} ga o`zgartirildi'
    except:
        return 'Siz ro`yxatdan o`tmagansiz iltimos ro`yxatdan o`ting'


def list_users():
    cursor.execute('SELECT * FROM users_table')
    return cursor.fetchall()


def delete_user_id(user_id):
    name = cursor.execute('SELECT first_name FROM users_table WHERE user_id=?', (user_id,)).fetchone()
    print(name)
    cursor.execute('DELETE FROM users_table WHERE user_id=?', (user_id,))
    connect.commit()
    return name
