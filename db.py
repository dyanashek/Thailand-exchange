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


# cursor.execute("DELETE FROM users WHERE id<>100")
# database.commit()

cursor.execute(f'''UPDATE referrals
                    SET amount=1
                    ''')

database.commit()

# l = 'NULL'
# cursor.execute(f'''
#             INSERT INTO users (user_id, user_username, referral)
#             VALUES ("4324235235", "dyanashek", "{None}")
#             ''')

# database.commit()

# print(cursor.execute("SELECT referral FROM users WHERE user_id<>111").fetchall())