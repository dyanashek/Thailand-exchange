import sqlite3
import logging
import inspect


def add_exchange(user_id, amount_currency, currency, amount_thb, current_time):
    try:
        database = sqlite3.connect("exchange.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = database.cursor()

        cursor.execute(f'''
            INSERT INTO exchanges (user_id, amount_currency, currency, amount_thb, status, rate_time)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, amount_currency, currency, amount_thb, 'creating', current_time,))
            
        database.commit()
        cursor.close()
        database.close()

        logging.info(f'{inspect.currentframe().f_code.co_name}: good.')

    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: bad. {ex}')


def select_exchange_info(exchange_id):
    try:
        database = sqlite3.connect("exchange.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = database.cursor()

        exchange_info = cursor.execute(f'''SELECT user_id, amount_currency, currency, amount_thb, status, rate_time
                                FROM exchanges
                                WHERE id=?
                                ''', (exchange_id,)).fetchall()[0]
        
        cursor.close()
        database.close

        return exchange_info
    
    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: bad. {ex}')


def get_creating_exchange_id(user_id):
    try:
        database = sqlite3.connect("exchange.db")
        cursor = database.cursor()

        exchange_id = cursor.execute(f'''SELECT id
                                FROM exchanges
                                WHERE user_id=? AND status=?
                                ''', (user_id, 'creating',)).fetchall()
        
        cursor.close()
        database.close

        if exchange_id:
            exchange_id = exchange_id[0][0]

        return exchange_id
    
    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: bad. {ex}')


def delete_exchange(exchange_id):
    try:
        database = sqlite3.connect("exchange.db")
        cursor = database.cursor()

        cursor.execute('DELETE FROM exchanges WHERE id=?', (exchange_id,))
        
        database.commit()
        cursor.close()
        database.close

    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: bad. {ex}')


def get_exchange_field_info(exchange_id, field):
    try:
        database = sqlite3.connect("exchange.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = database.cursor()

        info = cursor.execute(f'''SELECT {field}
                                FROM exchanges
                                WHERE id=?
                                ''', (exchange_id,)).fetchall()[0][0]
        
        cursor.close()
        database.close

        return info
    
    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: bad. {ex}')


def update_exchange_field_info(exchange_id, field, value):
    try:
        database = sqlite3.connect("exchange.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = database.cursor()

        cursor.execute(f'''UPDATE exchanges
                        SET {field}=?
                        WHERE id=?
                        ''', (value, exchange_id,))

        database.commit()
        cursor.close()
        database.close()

        logging.info(f'{inspect.currentframe().f_code.co_name}: good.')

    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: bad. {ex}')


def get_user_field_info(user_id, field):
    try:
        database = sqlite3.connect("exchange.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = database.cursor()

        info = cursor.execute(f'''SELECT {field}
                                FROM users
                                WHERE user_id=?
                                ''', (user_id,)).fetchall()[0][0]
        
        cursor.close()
        database.close

        return info
    
    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: bad. {ex}')


def update_user_field_info(user_id, field, value):
    try:
        database = sqlite3.connect("exchange.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = database.cursor()

        cursor.execute(f'''UPDATE users
                        SET {field}=?
                        WHERE user_id=?
                        ''', (value, user_id,))

        database.commit()
        cursor.close()
        database.close()

        logging.info(f'{inspect.currentframe().f_code.co_name}: good.')

    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: bad. {ex}')


def get_referral_field_info(referral, field):
    try:
        database = sqlite3.connect("exchange.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = database.cursor()

        info = cursor.execute(f'''SELECT {field}
                                FROM referrals
                                WHERE referral=?
                                ''', (referral,)).fetchall()[0][0]
        
        cursor.close()
        database.close

        return info
    
    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: bad. {ex}')


def update_referral_field_info(referral, field, value):
    try:
        database = sqlite3.connect("exchange.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = database.cursor()

        cursor.execute(f'''UPDATE referrals
                        SET {field}=?
                        WHERE referral=?
                        ''', (value, referral,))

        database.commit()
        cursor.close()
        database.close()

        logging.info(f'{inspect.currentframe().f_code.co_name}: good.')

    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: bad. {ex}')


def select_all_user_ids():
    try:
        database = sqlite3.connect("exchange.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = database.cursor()

        users_info = cursor.execute(f'''SELECT user_id, language
                                FROM users
                                ''').fetchall()
        
        cursor.close()
        database.close

        return users_info
    
    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: bad. {ex}')