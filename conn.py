import os
import sqlite3
import time
from datetime import datetime
from pathlib import Path

from queryes import (
    CREATE_TABLE_USERS,
    CREATE_TABLE_REVIEWS,
    DROP_TABLE_USERS,
    DROP_TABLE_REVIEWS,
    INSERT_USER,
    CHECK_ADMINS
)
from parse_data import insert_review
from reviews_data.fake_data import create_ten_review

### admins
ADMINS = [
    (5555555, 'ADMIN_1', 'ADMIN_1', True),
    (5555555, 'ADMIN_2', 'ADMIN_2', True),
    (5555555, 'ADMIN_3', 'ADMIN_3', True),
]


def setup_db():
    DB_PATH = './db.db'

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(DROP_TABLE_USERS)
    cursor.execute(DROP_TABLE_REVIEWS)

    cursor.execute(CREATE_TABLE_REVIEWS)
    cursor.execute(CREATE_TABLE_USERS)

    connection.commit()
    connection.close()


def admins():
    DB_PATH = './db.db'

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    for admin in ADMINS:
        cursor.execute(INSERT_USER, admin)

    all_admins = cursor.execute(CHECK_ADMINS, (True,)).fetchall()

    print(f'Admins: {all_admins}')

    connection.commit()
    connection.close()


if __name__ == '__main__':
    setup_db()
    admins()
    img = Path(__file__).resolve().parents[1] / 'files' / 'review_images'
    insert_review(create_ten_review(datetime.now()))
