import sqlite3
import logging

database = sqlite3.connect("exchange.db")
cursor = database.cursor()

try:
    # creates table with new users and their referrals
    cursor.execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        user_id VARCHAR (30),
        user_username VARCHAR (30),
        referral VARCHAR (30),
    )''')
except:
    logging.error('Users table already exists.')

try:
    # creates table with new users and their referrals
    cursor.execute('''CREATE TABLE referrals (
        id INTEGER PRIMARY KEY,
        identifier VARCHAR (30) DEFAULT NULL,
        referral VARCHAR (30),
        amount REAL DEFAULT 0
    )''')

except Exception as ex:
    print(ex)
    logging.error('Referrals table already exists.')


cursor.execute("DELETE FROM referrals WHERE id<>1000")
database.commit()