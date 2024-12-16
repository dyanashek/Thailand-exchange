import sqlite3
import logging
import inspect
import qrcode
import requests
import time
import datetime
import telebot

import utils
import classes
import config
import db_functions
import keyboards
import rates


bot = telebot.TeleBot(config.TELEGRAM_TOKEN)


def check_is_new_user(user_id):
    """Checks if user already in database. Returns True if he is a new user, False if not."""

    database = sqlite3.connect("exchange.db")
    cursor = database.cursor()

    users = cursor.execute(f'''SELECT COUNT(user_id) 
                                    FROM users 
                                    WHERE user_id="{user_id}"
                                    ''').fetchall()[0][0]
    
    cursor.close()
    database.close()

    if users == 0:
        return True
    
    return False


def add_user(user_id, user_username, referral=''):
    """Adds a new user to database."""

    database = sqlite3.connect("exchange.db")
    cursor = database.cursor()

    if referral == '':
        cursor.execute(f'''
            INSERT INTO users (user_id, user_username)
            VALUES (?, ?)
            ''', (user_id, user_username,))

    else:
        cursor.execute(f'''
            INSERT INTO users (user_id, user_username, referral)
            VALUES (?, ?, ?)
            ''', (user_id, user_username, referral,))
        
    database.commit()
    cursor.close()
    database.close()

    logging.info(f'{inspect.currentframe().f_code.co_name}: Добавлен новый пользователь {user_username}, реферал: {referral}.')
    
    
def handle_start_command(message):
    """Puts check_is_new_user and add_user together. Adds a new user if he is new.
    Checks the referral and adds it too if there is such referral.
    """

    user_id = message.from_user.id
    is_new_user = check_is_new_user(user_id)

    # if the user is new
    if is_new_user:

        referral = utils.extract_referral(message.text, '/start')
        is_referral = check_if_referral(referral)

        if not is_referral:
            referral = ''

        user_username = message.from_user.username
        add_user(user_id, user_username, referral)


def check_if_referral(referral):
    """Checks if there is such referral in database. Returns True if it is."""

    database = sqlite3.connect("exchange.db")
    cursor = database.cursor()

    referrals = cursor.execute(f'''SELECT COUNT(referral) 
                                    FROM referrals 
                                    WHERE referral="{referral}"
                                    ''').fetchall()[0][0]
    
    cursor.close()
    database.close()

    if referrals == 0:
        return False
    
    return True


def get_referral(referral):
    """Gets referral information from database."""

    database = sqlite3.connect("exchange.db")
    cursor = database.cursor()

    referral = cursor.execute(f'''SELECT identifier, referral, amount, percent
                                    FROM referrals 
                                    WHERE referral="{referral}"
                                    ''').fetchall()
    
    if referral != []:
        referral = classes.Referral(referral[0][0],
                                    referral[0][1],
                                    referral[0][2],
                                    referral[0][3],
                                    )
        
    return referral


def generate_qr(referral, user_id):
    referral_url = f'{config.BOT_LINK}?start={referral}'

    qr = qrcode.QRCode(version=1, 
                       error_correction=qrcode.constants.ERROR_CORRECT_L, 
                       box_size=10, 
                       border=2,
                       )

    # add data to qr
    qr.add_data(referral_url)

    qr_image = qr.make_image()

    qr_image.save(f'{user_id}.png')


def check_unique_identifier(identifier):
    """Checks the identifier is unique. Returns True if it is."""

    database = sqlite3.connect("exchange.db")
    cursor = database.cursor()

    referrals = cursor.execute(f'''SELECT COUNT(referral) 
                                    FROM referrals 
                                    WHERE identifier="{identifier}"
                                    ''').fetchall()[0][0]
    
    cursor.close()
    database.close()

    if referrals == 0:
        return True
    
    return False


def add_referral(identifier, referral):
    """Adds a new referral to database."""

    database = sqlite3.connect("exchange.db")
    cursor = database.cursor()

    cursor.execute(f'''
        INSERT INTO referrals (identifier, referral, percent)
        VALUES ("{identifier}", "{referral}", {config.REFERRAL_COEFF})
        ''')
    
    database.commit()
    cursor.close()
    database.close()

    logging.info(f'{inspect.currentframe().f_code.co_name}: Добавлен новый реферал {identifier}.')


def get_users_referral(username):
    """Gets users referral depends on his username."""

    database = sqlite3.connect("exchange.db")
    cursor = database.cursor()

    referral = cursor.execute(f"SELECT referral FROM users WHERE user_username='{username}'").fetchall()

    cursor.close()
    database.close()

    if referral != []:
        referral = referral[0][0]
        
        if referral is not None:
            return referral
    
    return False

        
def change_referral_amount(referral, amount):
    """Changes referrals amount."""

    database = sqlite3.connect("exchange.db")
    cursor = database.cursor()

    cursor.execute(f'''UPDATE referrals
                    SET amount={amount}
                    WHERE referral="{referral}"
                    ''')

    database.commit()
    cursor.close()
    database.close()

    logging.info(f'{inspect.currentframe().f_code.co_name}: Сумма выплаты рефералу {referral} изменена на {amount}.')


def get_all_referrals():
    """Extract all referrals."""

    database = sqlite3.connect("exchange.db")
    cursor = database.cursor()

    referrals = cursor.execute("SELECT * FROM referrals").fetchall()

    cursor.close()
    database.close()

    return referrals


def construct_all_referrals_message(referrals):
    """Constructs message that contains information about all referrals."""

    replies = []
    count = 0
    reply_text = ''

    for num, referral in enumerate(referrals):
        amount = utils.numbers_format(referral[3])
        reply_text += f'{num + 1}. У *{referral[2]}* ({utils.escape_markdown(referral[1])}) на счету *{amount}* бат, бонус *{int(referral[4] * 100)}%*.\n'
        count += 1

        if count == 50 or count == len(referrals):
            replies.append(reply_text)
            reply_text = ''
            count = 0
    
    return replies


def reduce_all_referrals_balance():
    """Reduces all referrals balances to 0."""

    database = sqlite3.connect("exchange.db")
    cursor = database.cursor()

    cursor.execute("UPDATE referrals SET amount=0")

    database.commit()
    cursor.close()
    database.close()

    logging.info(f'{inspect.currentframe().f_code.co_name}: Счета всех рефералов обнулены.')


def reduce_referral_balance(referral):
    """Reduces all referrals balances to 0."""

    database = sqlite3.connect("exchange.db")
    cursor = database.cursor()

    cursor.execute(f"UPDATE referrals SET amount=0 WHERE referral='{referral}'")

    database.commit()
    cursor.close()
    database.close()

    logging.info(f'{inspect.currentframe().f_code.co_name}: Счета реферала {referral} обнулены.')


# def p2p_binance(currency = 'THB', amount = ''):
#     """Gets price of buying or selling usdt on Binance p2p."""

#     # indicate trade side
#     side = '1'
#     if currency == 'THB':
#         side = '0'
    
#     pay_types = []
#     if currency == 'RUB':
#         pay_types = ['64', '75', '14']
#     elif currency == 'THB':
#         pay_types = ['14']

#     # construct params
#     data_binance = {
#         "tokenId": config.COIN,
#         "currencyId": currency,
#         "authMaker" : "true",
#         "side": side,
#         "amount": amount,
#         "payment" : pay_types,
#         "userId" : "",
#     }
#     # make a request
#     try:
#         deals = requests.post(url=config.URL_BINANCE, data=data_binance, headers=config.HEADERS).json().get('result').get('items')
#     except:
#         deals = None
    
#     if deals is not None:

#         for deal in deals:
#             # extract merchants order count and rate
#             order_count = int(deal.get('recentOrderNum'))
#             finish_rate = float(deal.get('recentExecuteRate'))

#             # extract price if the merchant fits params
#             if order_count >= config.ORDERS and finish_rate >= config.ORDERS_RATE:
#                 price = float(deal.get('price'))

#                 return price
    
#     return None

def get_rub_price():
    data_bybit = {
        'tokenId': 'USDT', 
        'currencyId': 'RUB', 
        'payment': ['581',],
        'amount' : '',
        'side' : '1',
        # 'authMaker' : 'true',
    }

    headers = {
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'origin' : 'https://www.bybit.com'
    }

    try:
        deals = requests.post(url='https://api2.bybit.com/fiat/otc/item/online', data=data_bybit, headers=headers).json().get('result').get('items')
    except:
        return 'Ошибка соединения'
    
    if deals is None:
        return 'Ошибка соединения'
    
    for deal in deals:
        order_count = int(deal.get('recentOrderNum'))
        finish_rate = float(deal.get('recentExecuteRate'))
        if order_count >= 50 and finish_rate >= 0.96:
            return float(deal.get('price'))


def p2p_binance(currency = 'THB', amount = ''):
    """Gets price of buying or selling usdt on Binance p2p."""

    # indicate trade side
    side = 'BUY'
    if currency == 'THB':
        side = 'SELL'
    
    pay_types = []
    if currency == 'THB':
        pay_types = ["BANK"]

    # construct params
    data_binance = {
        "asset": config.COIN,
        "countries": [],
        "fiat": currency,
        "page": 1,
        "proMerchantAds": False,
        "publisherType": "merchant",
        "rows": 20,
        "tradeType": side,
        "transAmount": amount,
        "payTypes" : pay_types,
    }

    # make a request
    try:
        deals = requests.post(url=config.URL_BINANCE, json=data_binance, headers=config.HEADERS).json().get('data')
    except:
        deals = None
    
    if deals is not None:

        for deal in deals:
            # extract merchants order count and rate
            order_count = int(deal.get('advertiser').get('monthOrderCount'))
            finish_rate = float(deal.get('advertiser').get('monthFinishRate'))

            # extract price if the merchant fits params
            if order_count >= config.ORDERS and finish_rate >= config.ORDERS_RATE:
                price = float(deal.get('adv').get('price'))

                return price


def get_basic_exchange_rate(currency):
    """Gets minimal rate for currency pair."""

    thb_price = p2p_binance()

    if currency == 'RUB':
        rub_price = get_rub_price()
        rate = round(rub_price / thb_price, 3)

    elif currency == 'USD':
        usd_price = p2p_binance(currency)
        rate = round(thb_price / usd_price, 3)
    
    elif currency == 'USDT':
        rate = round(thb_price, 3)

    return rate


def set_basic_exchange_rate():
    """Sets basic rates in a loop."""

    while True:
        try:
            config.BASIC_USD = get_basic_exchange_rate('USD')
            config.BASIC_USDT = get_basic_exchange_rate('USDT')
            config.BASIC_RUB = get_basic_exchange_rate('RUB')
        except:
            pass

        time.sleep(15)


def get_exchange_rate(currency, delivery_type, amount_currency='THB', amount=''):
    """Calculates exchange rates depends on amounts and type of delivery."""

    if amount == '':
        amount = config.TYPE_AMOUNT[delivery_type]
    
    coeff = config.TYPE_COEFF[delivery_type]

    try:
        if amount_currency == 'THB':
            # amount = 40000
            thb_price = p2p_binance(amount=amount)
            if currency == 'RUB':
                rub_amount = round(amount * config.BASIC_RUB, 2)
                rub_price = get_rub_price()

                rate = round(rub_price / thb_price * coeff, 3) 
            
            elif currency == 'USD':
                usd_amount = round(amount / config.BASIC_USD, 2)
                usd_price = p2p_binance(currency='USD', amount=usd_amount)

                rate = round(thb_price / usd_price / coeff, 3) 
            
            elif currency == 'USDT':
                rate = round(thb_price / coeff, 3) 
        
        else:
            if currency == 'RUB':
                rub_price = get_rub_price()
                thb_amount = round(amount / config.BASIC_RUB, 2)
                thb_price = p2p_binance(amount=thb_amount)

                rate = round(rub_price / thb_price * coeff, 3) 
            
            elif currency == 'USD':
                usd_price = p2p_binance(currency='USD', amount=amount)
                thb_amount = round(amount * config.BASIC_USD, 2)
                thb_price = p2p_binance(amount=thb_amount)

                rate = round(thb_price / usd_price / coeff, 3) 

            elif currency == 'USDT':
                thb_amount = round(amount * config.BASIC_USDT, 2)
                thb_price = p2p_binance(amount=thb_amount)
                
                rate = round(thb_price / coeff, 3) 
    except:
        rate = None

    return rate


def set_specific_exchange_rate():
    while True:
        try:
            rates.RUB_DELIVERY_RATE = get_exchange_rate('RUB', 'delivery')
            rates.RUB_AIRPORT_RATE = get_exchange_rate('RUB', 'airport')
            rates.RUB_ATM_RATE = get_exchange_rate('RUB', 'atm')
            rates.RUB_OFFICE_RATE = get_exchange_rate('RUB', 'office')
            rates.RUB_TRANSFER_RATE = get_exchange_rate('RUB', 'transfer')
            rates.RUB_SERVICE_RATE = get_exchange_rate('RUB', 'service')
            
            rates.USDT_DELIVERY_RATE = get_exchange_rate('USDT', 'delivery')
            rates.USDT_AIRPORT_RATE = get_exchange_rate('USDT', 'airport')
            rates.USDT_ATM_RATE = get_exchange_rate('USDT', 'atm')
            rates.USDT_OFFICE_RATE = get_exchange_rate('USDT', 'office')
            rates.USDT_TRANSFER_RATE = get_exchange_rate('USDT', 'transfer')
            rates.USDT_SERVICE_RATE = get_exchange_rate('USDT', 'service')

            rates.USD_DELIVERY_RATE = get_exchange_rate('USD', 'delivery')
            rates.USD_AIRPORT_RATE = get_exchange_rate('USD', 'airport')
            rates.USD_ATM_RATE = get_exchange_rate('USD', 'atm')
            rates.USD_OFFICE_RATE = get_exchange_rate('USD', 'office')
            rates.USD_TRANSFER_RATE = get_exchange_rate('USD', 'transfer')
            rates.USD_SERVICE_RATE = get_exchange_rate('USD', 'service')
        except:
            pass

        time.sleep(60)


def currency_rate_message(language):
    """Generates a message with currency rates and terms of use."""

    current_date = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime("%d.%m.%Y")

    if language == 'rus':
        text = f'''
            \n*Курс на {current_date}* 🗓\
            \n\
            \n💱 *THB/RUB*:\
            \nВыдача через банкомат - *{rates.RUB_ATM_RATE}*\
            \nОплата услуг - *{rates.RUB_TRANSFER_RATE}*\
            \nПеревод на тайский счет - *{rates.RUB_TRANSFER_RATE}*\
            \nКурьерская доставка (500 THB) - *{rates.RUB_DELIVERY_RATE}*\
            \n\
            \n💰 *USDT/THB*:\
            \nВыдача через банкомат - *{rates.USDT_ATM_RATE}*\
            \nОплата услуг - *{rates.USDT_TRANSFER_RATE}*\
            \nПеревод на тайский счет - *{rates.USDT_TRANSFER_RATE}*\
            \nКурьерская доставка (500 THB) - *{rates.USDT_DELIVERY_RATE}*\
            \n\
            \n*Минимальная сумма выдачи*:\
            \nЧерез банкомат от *1 000 THB*\
            \nНа тайский счет от *1 000 THB*\
            \nОплата услуг от *1 000 THB*\
            \nСтоимость курьерской доставки *500 THB*\
            \n\
            \n❗️*ВАЖНО*❗️\
            \nВ сообщении представлены справочные данные. Курс меняется в режиме реального времени и может отличаться в зависимости от суммы обмена. Для более точного расчета воспользуйтесь кнопкой *обмен валюты* в меню.\
        '''
    else:
        text = f'''
            \n*Course to {current_date}* 🗓\
            \n\
            \n💱 *THB/RUB*:\
            \nWithdrawal via ATM - *{rates.RUB_ATM_RATE}*\
            \nTransfer to Thai account - *{rates.RUB_TRANSFER_RATE}*\
            \nPayment for services - *{rates.RUB_TRANSFER_RATE}*\
            \nCourier delivery (500 THB) - *{rates.RUB_DELIVERY_RATE}*\
            \n\
            \n💰 *USDT/THB*:\
            \nATM withdrawal - *{rates.USDT_ATM_RATE}*\
            \nTransfer to Thai account - *{rates.USDT_TRANSFER_RATE}*\
            \nPayment for services - *{rates.USDT_TRANSFER_RATE}*\
            \nCourier delivery (500 THB)- *{rates.USDT_DELIVERY_RATE}*\
            \n\
            \n*Minimum withdrawal amount*:\
            \nVia ATM from *1 000 THB*\
            \nTo Thai account from *1 000 THB*\
            \nPayment for services from *1 000 THB*\
            \n\
            \n❗️*IMPORTANT*❗️\
            \nThe message contains reference data. The rate changes in real time and may differ depending on the amount of the exchange. For a more accurate calculation, use the *currency exchange* button in menu.\
        '''

    return text


def set_language(user_id, language):
    """Sets users language."""

    database = sqlite3.connect("exchange.db")
    cursor = database.cursor()

    cursor.execute(f'''UPDATE users
                    SET language="{language}"
                    WHERE user_id="{user_id}"
                    ''')

    database.commit()
    cursor.close()
    database.close()


def get_language(user_id):
    '''Gets users language.'''

    database = sqlite3.connect("exchange.db")
    cursor = database.cursor()

    language = cursor.execute(f"SELECT language FROM users WHERE user_id='{user_id}'").fetchall()

    cursor.close()
    database.close()

    if language:
        language = language[0][0]
    else:
        language = 'rus'
    
    return language


def currency_rate_notification(language):
    """Generates a message with currency rates and terms of use."""

    current_date = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime("%d.%m.%Y")

    if language == 'rus':
        text = f'''
            \n*Курс на {current_date}* 🗓\
            \n\
            \n💱 *THB/RUB*:\
            \nКурьерская доставка - *{rates.RUB_DELIVERY_RATE}*\
            \nВыдача через банкомат - *{rates.RUB_ATM_RATE}*\
            \nПеревод на тайский счет - *{rates.RUB_TRANSFER_RATE}*\
            \n\
            \n💰 *USDT/THB*:\
            \nКурьерская доставка - *{rates.USDT_DELIVERY_RATE}*\
            \nВыдача через банкомат - *{rates.USDT_ATM_RATE}*\
            \nПеревод на тайский счет - *{rates.USDT_TRANSFER_RATE}*\
            \n\
            \n❗️*ВАЖНО*❗️\
            \nВ сообщении представлены справочные данные. Курс меняется в режиме реального времени и может отличаться в зависимости от суммы обмена. Для более точного расчета воспользуйтесь кнопкой *обмен валюты* в меню.\
        '''
    else:
        text = f'''
            \n*Course to {current_date}* 🗓\
            \n\
            \n💱 *THB/RUB*:\
            \nCourier delivery - *{rates.RUB_DELIVERY_RATE}*\
            \nWithdrawal via ATM - *{rates.RUB_ATM_RATE}*\
            \nTransfer to Thai account - *{rates.RUB_TRANSFER_RATE}*\
            \n\
            \n💰 *USDT/THB*:\
            \nCourier delivery - *{rates.USDT_DELIVERY_RATE}*\
            \nATM withdrawal - *{rates.USDT_ATM_RATE}*\
            \nTransfer to Thai account - *{rates.USDT_TRANSFER_RATE}*\
            \n\
            \n❗️*IMPORTANT*❗️\
            \nThe message contains reference data. The rate changes in real time and may differ depending on the amount of the exchange. For a more accurate calculation, use the *currency exchange* button in main menu.\
        '''

    return text

def daily_notify():
    while True:
        current_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime("%H:%M")

        if current_time == '11:00':
            users_info = db_functions.select_all_user_ids()

            for user_info in users_info:
                try:
                    bot.send_message(chat_id=user_info[0],
                                     text=currency_rate_notification(user_info[1]),
                                     reply_markup=keyboards.menu_keyboard(user_info[1]),
                                     parse_mode='Markdown',
                                     disable_notification=False,
                                     )
                except:
                    pass
            
            time.sleep(86250)

def send_marketing_message(text, content_type, media_id=None):
    users_ids = db_functions.select_all_user_ids()

    for user_id in users_ids:
        if content_type == 'text':
            try:
                bot.send_message(chat_id=user_id[0],
                                 text=text,
                                 disable_notification=False,
                                 )
            except:
                pass

        elif content_type == 'photo':
            try:
                bot.send_photo(chat_id=user_id,
                               caption=text,
                               photo=media_id,
                               disable_notification=False,
                               )
            except:
                pass

        elif content_type == 'video':
            try:
                bot.send_video(chat_id=user_id,
                               caption=text,
                               video=media_id,
                               disable_notification=False,
                               )
            except:
                pass

# \nПолучение в офисе - *{rates.RUB_OFFICE_RATE}*\

# \nПолучение в офисе - *{rates.USDT_OFFICE_RATE}*\

# \n\
# \n💵 *USD/THB*:\
# \nКурьерская доставка - *{rates.USD_DELIVERY_RATE}*\
# \nДоставка в аэропорт - *{rates.USD_AIRPORT_RATE}*\
# \nВыдача через банкомат - *{rates.USD_ATM_RATE}*\
# \nПолучение в офисе - *{rates.USD_OFFICE_RATE}*\
# \nПеревод на тайский счет - *{rates.USD_TRANSFER_RATE}*\
# \nОплата услуг - *{rates.USD_TRANSFER_RATE}*\

# \nВ офисе от *5 000 THB*\