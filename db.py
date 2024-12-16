import sqlite3
import logging

database = sqlite3.connect("exchange.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
cursor = database.cursor()

try:
    # creates table with new users and their referrals
    cursor.execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        user_id VARCHAR (30),
        user_username VARCHAR (30),
        referral VARCHAR (30),
        language TEXT,
        input_data TEXT
    )''')
except:
    logging.error('Users table already exists.')

try:
    # creates table with new users and their referrals
    cursor.execute('''CREATE TABLE referrals (
        id INTEGER PRIMARY KEY,
        identifier VARCHAR (30) DEFAULT NULL,
        referral VARCHAR (30),
        amount REAL DEFAULT 0,
        percent REAL DEFAULT 0.1
    )''')

except Exception as ex:
    print(ex)
    logging.error('Referrals table already exists.')

try:
    # creates table with new users and their referrals
    cursor.execute('''CREATE TABLE exchanges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        amount_currency REAL,
        currency TEXT,
        amount_thb REAL,
        status TEXT,
        rate_time TIMESTAMP
    )''')
except:
    logging.error('Users table already exists.')
    