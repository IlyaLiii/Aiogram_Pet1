DROP_TABLE_USERS = '''
        DROP TABLE IF EXISTS Users
    '''

DROP_TABLE_REVIEWS = '''
        DROP TABLE IF EXISTS Reviews
    '''

CREATE_TABLE_USERS = '''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            login VARCHAR(100) NOT NULL,
            password VARCHAR(100) NOT NULL,
            is_admin BOOLEAN NOT NULL
        );
    '''
CREATE_TABLE_REVIEWS = '''
        CREATE TABLE IF NOT EXISTS Reviews (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            date DATE NOT NULL,
            text TEXT BOOLEAN NOT NULL,
            photo BLOB UNIQUE
        );
    '''
INSERT_USER = "INSERT INTO Users VALUES (null, ?, ?, ?, ?)"

CHECK_ADMINS = '''
        SELECT user_id FROM Users
        WHERE `is_admin` = ?
    '''

CHECK_USER = 'SELECT * FROM `Users` WHERE `password` = ? AND `login` = ?'

DOWNLOAD_LOGPASS = '''
        SELECT login, password 
        FROM Users
        WHERE `is_admin` = ?
    '''

GET_REVIEWS = '''
    SELECT name, date, text, photo FROM `Reviews`
    '''

GET_LAST_FIVE_REVIEWS = '''
    SELECT name, date, text, photo FROM `Reviews` WHERE `date` >= ? LIMIT 5
    '''
INSERT_REVIEWS = '''
    INSERT INTO Reviews VALUES (null, ?, ?, ?, ?)
    '''

