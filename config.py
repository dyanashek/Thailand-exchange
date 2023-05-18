import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# manager's id (redirect users to him)
MANAGER_ID = '877069241' # change !!!

# manager's username
MANAGER_USERNAME = 'dyanashek' # change !!!

# director's id - gets all reports
DIRECTOR_ID = '5855351963'

# bot's link
BOT_LINK = 'https://t.me/XChange_money_bot'

# bot's ID
BOT_ID = '6089617766'

# profit that we gets from every exchange
PROFIT_COEFF = 0.02

# amount that referral gets
REFERRAL_COEFF = 0.1

# headers for requests
HEADERS = {
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
}

# binance url for requests
URL_BINANCE = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'

# minimal orders count for binance p2p
ORDERS = 10

# minimal orders rate for binance p2p
ORDERS_RATE = 0.95

# banks for binance p2p
BANKS = ['TinkoffNew']

# coin for binance p2p
COIN = 'USDT'

# basic rate of currencies to THB
BASIC_USD = 34.0
BASIC_USDT = 33.9
BASIC_RUB = 2.4

# types of delivery and their coeff
TYPE_COEFF ={
    'delivery' : 1.025,
    'airport' : 1.025,
    'atm' : 1.022,
    'office' : 1.021,
    'transfer' : 1.02,
    'service' : 1.02,
}

# types of delivery and their minimal amount
TYPE_AMOUNT ={
    'delivery' : 40000,
    'airport' : 40000,
    'atm' : 10000,
    'office' : 5000,
    'transfer' : 5000,
    'service' : 5000,
}

# types of delivery with translation
TYPE_RUSSIAN ={
    'delivery' : 'курьер',
    'airport' : 'аэропорт',
    'atm' : 'банкомат',
    'office' : 'офис',
    'transfer' : 'перевод на тайский счет',
    'service' : 'оплата услуг',
}

# message that displays when referral is incorrect
INCORRECT_REFERRAL_MESSAGE = 'Предоставленный реферал содержит недопустимые символы. Реферал должен состоять *только из букв латинского алфавита и цифр*.'

# part of message that should be in reply message to register identifier
CHECK_IDENTIFIER = 'в ответ на это сообщение укажите имя или название компании'

# message that displays if user doesn't have referral
NO_REFERRAL_MESSAGE = 'У пользователя нет реферала.'

# message that displays when manager provided wrong format of data, when adding amount to referral
WRONG_FORMAT_MESSAGE = 'Неверный формат команды.'

# message that displays if user doesn't have permissions to proceed the command
NO_PERMISSION_MESSAGE = 'Недостаточно прав для совершения действия.'

# message that displays when user press 'cancel' button
CANCEL_MESSAGE = 'Действие отменено.'

# message that displays if there is not such referral
WRONG_REFERRAL_MESSAGE = 'Такого реферала не обнаружено.'

# message that displays when director wants to set all referrals balance to 0
REDUCE_BALANCE_MESSAGE = 'Обнулить счета всех рефералов?'

# message that displays when director reduced all referrals balance to 0
REDUCED_BALANCE_MESSAGE = 'Cчета всех рефералов обнулены.'

# message that displays with main menu
MAIN_MENU_MESSAGE = 'Выберите интересующий вас раздел:'

# message that displays when user wants to know more about special services
SERVICE_MESSAGE = '''
            \nС помощью нашего сервиса вы можете воспользоваться следующими услугами:\
            \n\
            \n💰 Обмен валюты на *крупные суммы* - *специальный курс*\
            \n\
            \n💻 Обмен валюты для *бизнеса* - *специальный курс*\
            \n\
            \n💳 Валютные переводы между странами\
            \n\
            \nДля уточнения подробностей *свяжитесь с менеджером* с помощью кнопки ниже.\
            '''

# message that displays when user chooses faq section
QUESTION_MESSAGE = 'Выберите интересующий вас вопрос:'

# message that displays when user wants to get details about ATM exchange
ATM_MESSAGE = '''
            \nБанкоматы Таиланда позволяют удаленно выдавать наличные с помощью QR-кода. На сегодняшний день наш сервис работает со следующими банками:\
            \n\
            \n- *BANGKOK BANK* 🏦\
            \n- *BANK OF AYUDHYA (KRUNGSRI)* 🏦\
            \n- *KASIKORNBANK* 🏦\
            \n\
            \n❗️ Доступно при обмене от *10 000 THB*. Сумма в батах должна быть кратна 100.\
            \n\
            \nПодробную инструкцию по использованию вы можете скачать с помощью кнопки ниже ⬇️\
            '''

# message that displays when user wants to get details about airport delivery
AIRPORT_MESSAGE = '''
            \nМы поможем вам получить наличные баты *сразу по прилете* в Таиланд!\
            \n\
            \nЗакажите такси из аэропорта до места своего размещения, где вас уже будет ждать наш курьер с необходимой суммой.\
            \n\
            \nМы поможем оплатить ваше такси через qr код водителя, не переживайте за это.\
            \n\
            \n❗️ Работаем на Пхукете. Доступно при обмене от *40 000 THB*.\
            '''

# message that displays when user wants to get details about delivery
DELIVERY_MESSAGE = '''
            \nПриедем и передадим наличные лично в руки: *удобно и безопасно*.\
            \n\
            \n❗️ Работаем на Пхукете. Доступно при обмене от *40 000 THB*.\
            '''

# message that displays when user wants to get details about transfer
TRANSFER_MESSAGE = '''
            \nПоможем вам оплатить *крупную покупку*, *бронирование отеля*, *авиабилетов* и многое другое. Рассчитываетесь с нами, получаете оплаченную услугу! *Удобно и просто*.\
            \n\
            \n❗️ Доступно при оплате услуг от *5 000 THB*.\
            '''

# message that displays when user wants to know more about banks
BANKS_MESSAGE = '''
                \nВоспользоваться нашими услугами можно, выполнив перевод любым из удобных вам способов:\
                \n\
                \n- *РАЙФФАЙЗЕН БАНК* 🏦\
                \n- *ТИНЬКОФФ* 🏦\
                \n- *СБЕР* 🏦\
                \n- *СБП* 🏦\
                '''

# file id with instruction of using bangkok bank atm
BANGKOK_FILE = 'BQACAgIAAxkBAAMFZGW71NNkl2IAAQPBHvb5TFOFzYexAALvMgACRbcpSxaDV9BMqOMDLwQ'

# file id with instruction of using kasikorn bank atm
KASIKORN_FILE ='BQACAgIAAxkBAAMEZGW7t3z_xWSPivyvxayTi9yX9QkAAukyAAJFtylL_mnyI0cNjT0vBA'

# file id with instruction of using krungsri bank atm
KRUNGSRI_FILE = '' # add !!!

# message to choose currency pair
PAIRS_MESSAGE = 'Выберите пару для обмена:'

# message to exchange type
EXCHANGE_TYPE_MESSAGE = 'Выберите удобный способ обмена:'

# part of message that added when user gets the rate
ADDITIONAL_MESSAGE = '❗️ Для совершения обмена подтвердите свою заявку с помощью кнопки ниже ⬇️'