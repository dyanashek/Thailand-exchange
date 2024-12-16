import sqlite3

database = sqlite3.connect("exchange.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
cursor = database.cursor()

cursor.execute('ALTER TABLE referrals ADD COLUMN percent REAL DEFAULT 0.3')

database.commit()
cursor.close()
database.close()