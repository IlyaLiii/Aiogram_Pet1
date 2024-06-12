import logging
import sqlite3
from datetime import datetime, timedelta

from queryes import INSERT_USER, CHECK_USER, CHECK_ADMINS, DOWNLOAD_LOGPASS, GET_REVIEWS, INSERT_REVIEWS, \
    GET_LAST_FIVE_REVIEWS

FILE_LOG_PASS = 'files/log:pass.txt'


def is_user_exist(data):
    DB_PATH = './db.db'

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor = connection.cursor()

    login = data.get('login')
    password = data.get('password')

    check_user = cursor.execute(CHECK_USER, (password, login,)).fetchone()
    print(check_user)

    # return True if check_user is not None else False
    if check_user is not None:
        return True
    else:
        return False


def insert_user(data):
    logging.info(data)
    DB_PATH = './db.db'

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    user_id = data.get('user_id')
    login = data.get('login')
    password = data.get('password')

    cursor.execute(INSERT_USER, (user_id, login, password, False,))

    connection.commit()
    connection.close()

    return f'INSERT {login}:{password} successful'


def export_admins():
    DB_PATH = './db.db'

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    export_admins = cursor.execute(CHECK_ADMINS, (True,)).fetchall()

    list_admins = []
    for admin in export_admins:
        list_admins.append(admin[0])

    return list_admins


def create_log_pass_txt():
    DB_PATH = './db.db'

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    log_pass_data = cursor.execute(DOWNLOAD_LOGPASS, (False,)).fetchall()

    if len(log_pass_data) > 0:
        list_data = []
        for i in log_pass_data:
            list_data.append(f'{i[0]} : {i[1]}')

        with open(FILE_LOG_PASS, 'w') as file:
            for line in list_data:
                file.write(line + '\n')

        return True

    else:
        return False


def get_reviews() -> list:
    DB_PATH = './db.db'

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    query = cursor.execute(GET_REVIEWS, ).fetchall()

    connection.commit()
    connection.close()

    return query


def get_last_five_reviews() -> list:
    DB_PATH = './db.db'

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    query = cursor.execute(GET_LAST_FIVE_REVIEWS,
                           (datetime.now() - timedelta(days=2),)).fetchall()

    connection.commit()
    connection.close()

    return query


def insert_review(data) -> None:
    DB_PATH = './db.db'

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    for review in data:

        name = review[0]
        date = review[1]
        text = review[2]
        photo = review[3]

        cursor.execute(INSERT_REVIEWS, (name, date, text, photo,))

        print(f'Name: {name} insert in review')

    connection.commit()
    connection.close()