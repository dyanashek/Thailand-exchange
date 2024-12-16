import os
from dotenv import load_dotenv
import telebot

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

BANK = 'Тинькофф'
ACCOUNT = '1111 1111 1111 1111'
NUMBER = '89991111111'
RECEIVER = 'Петров Петр'

MAX_AMOUNT = 25000
# manager's id (redirect users to him)
MANAGER_ID = ['7754317393',] # change !!!

# manager's username
MANAGER_USERNAME = 'ELnur828' # change !!!

# director's id - gets all reports
DIRECTOR_ID = '7754317393'

# bot's link
BOT_LINK = 'https://t.me/EVAexchange_bot'

# bot's ID
BOT_ID = '7585049275'

TG_CHANNEL = 'https://t.me/EVA_exvhange'

INSTAGRAM = 'https://instagram.com/eva_exchange_?igsh=MzRlODBiNWFlZA=='


# profit that we gets from every exchange
PROFIT_COEFF = 0.02

# amount that referral gets
REFERRAL_COEFF = 0.3

ADDRESS_GOOGLE_MAPS = 'https://maps.app.goo.gl/Q1z7krkiU9XQghzdA?g_st=com.google.maps.preview.copy'

OFFICE_PHOTO = 'AgACAgIAAxkBAAPPZ1_13FXgbjL1DdVdj_jeK04Q7_UAAijkMRtnQAFLkMsZjEWlVH4BAAMCAAN5AAM2BA'

# headers for requests
HEADERS = {
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'origin' : 'https://www.bybit.com',
}

# binance url for requests
# URL_BINANCE = 'https://api2.bybit.com/fiat/otc/item/online'
URL_BINANCE = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'

url_binance_spot = 'https://api.binance.com/api/v3/ticker/price?symbol='

RUB_COEFF = 1.013

CRYPTO_WALLET = 'TNotLBH8TBiW738k89D3j4YsdZ3WsmkHAy'

# minimal orders count for binance p2p
ORDERS = 10

# minimal orders rate for binance p2p
ORDERS_RATE = 0.95

# banks for binance p2p
BANKS = ['64']

# coin for binance p2p
COIN = 'USDT'

# basic rate of currencies to THB
BASIC_USD = 33.5
BASIC_USDT = 33.5
BASIC_RUB = 3

# types of delivery and their coeff
TYPE_COEFF ={
    'delivery' : 1.028,
    'kata' : 1.028,
    'ravai' : 1.028,
    'patong' : 1.028,
    'chalong' : 1.028,
    'portarea' : 1.028,
    'airport' : 1.028,
    'atm' : 1.025,
    'office' : 1.024,
    'transfer' : 1.023,
    'service' : 1.023,
}

# types of delivery and their minimal amount
TYPE_AMOUNT ={
    'delivery' : 1000,
    'kata' : 1000,
    'ravai' : 1000,
    'patong' : 1000,
    'chalong' : 1000,
    'portarea' : 1000,
    'airport' : 1000,
    'atm' : 1000,
    'office' : 1000,
    'transfer' : 1000,
    'service' : 1000,
}

# types of delivery with translation
TYPE_RUSSIAN ={
    'delivery' : 'курьер (доставка)',
    'kata' : 'курьер (Ката/Карон)',
    'ravai' : 'курьер (Равай/Найхарн)',
    'patong' : 'курьер (Патонг/Кату)',
    'chalong' : 'курьер (Чалонг)',
    'portarea' : 'курьер (Зона аэропорта)',
    'airport' : 'аэропорт',
    'atm' : 'банкомат',
    'office' : 'офис',
    'transfer' : 'перевод на тайский счет',
    'service' : 'оплата услуг',
}
TYPE_ENGLISH ={
    'delivery' : 'courier (delivery)',
    'kata' : 'courier (Kata)',
    'ravai' : 'courier (Rawai/Niharn)',
    'patong' : 'courier (Patong/Katu)',
    'chalong' : 'courier (Chalong)',
    'portarea' : 'courier (Airport area)',
    'airport' : 'airport',
    'atm' : 'ATM',
    'office' : 'office',
    'transfer' : 'transfer to Thai account',
    'service' : 'payment for services',
}

CHOOSE_LANGUAGE = 'Выберите ваш язык / Choose your language:'

# message that displays when referral is incorrect
INCORRECT_REFERRAL_MESSAGE = {
    'rus' : 'Предоставленный реферал содержит недопустимые символы. Реферал должен состоять *только из букв латинского алфавита и цифр*.',
    'eng' : 'The provided referral contains invalid characters. Referral must consist of *only Latin letters and numbers*.',
}

# part of message that should be in reply message to register identifier
CHECK_IDENTIFIER = {
    'rus' : 'в ответ на это сообщение укажите имя или название компании',
    'eng' : 'in response to this message, enter your name or company name',
}

# message that displays if user doesn't have referral
NO_REFERRAL_MESSAGE = {
    'rus' : 'У пользователя нет реферала.',
    'eng' : 'User does not have a referral.',
}

# message that displays when manager provided wrong format of data, when adding amount to referral
WRONG_FORMAT_MESSAGE = {
    'rus' : 'Неверный формат команды.',
    'eng' : 'Invalid command format.',
}

# message that displays if user doesn't have permissions to proceed the command
NO_PERMISSION_MESSAGE = {
    'rus' : 'Недостаточно прав для совершения действия.',
    'eng' : 'Insufficient rights to perform the action.',
}

# message that displays when user press 'cancel' button
CANCEL_MESSAGE = {
    'rus' : 'Действие отменено.',
    'eng' : 'Action cancelled.',
}

# message that displays if there is not such referral
WRONG_REFERRAL_MESSAGE = {
    'rus' : 'Такого реферала не обнаружено.',
    'eng' : 'No such referral found.',
}

# message that displays when director wants to set all referrals balance to 0
REDUCE_BALANCE_MESSAGE = {
    'rus' : 'Обнулить счета всех рефералов?',
    'eng' : 'Reset accounts of all referrals?',
}

# message that displays when director reduced all referrals balance to 0
REDUCED_BALANCE_MESSAGE = {
    'rus' : 'Cчета всех рефералов обнулены.',
    'eng' : 'All referral accounts have been reset.',
}

# message that displays with main menu
MAIN_MENU_MESSAGE = {
    'rus' : 'Выберите интересующий вас раздел:',
    'eng' : 'Select the section you are interested in:',
}

# message that displays when user wants to know more about special services
SERVICE_MESSAGE = {
    'rus' : '''
            \nС помощью нашего сервиса вы можете воспользоваться следующими услугами:\
            \n\
            \n💰 Обмен валюты на *крупные суммы* - *специальный курс*\
            \n\
            \n💻 Обмен валюты для *бизнеса* - *специальный курс*\
            \n\
            \n💳 Валютные переводы между странами\
            \n\
            \nДля уточнения подробностей *свяжитесь с менеджером* с помощью кнопки ниже.\
            ''',
    'eng' : '''
            \nWith our help you can use the following services:\
            \n\
            \n💰 Currency exchange for *large amounts* - *special rate*\
            \n\
            \n💻 Currency exchange for *business* - *special rate*\
            \n\
            \n💳 Currency transfers between countries\
            \n\
            \nFor more details, *contact the manager* using the button below.\
            ''',
}

# message that displays when user chooses faq section
QUESTION_MESSAGE = {
    'rus' : 'Выберите интересующий вас вопрос:',
    'eng' : 'Select the question you are interested in:',
}

# message that displays when user wants to get details about ATM exchange
ATM_MESSAGE = {
    'rus' : '''
            \nБанкоматы Таиланда позволяют удаленно выдавать наличные с помощью QR-кода. На сегодняшний день наш сервис работает со следующими банками:\
            \n\
            \n- *BANGKOK BANK* 🏦\
            \n- *BANK OF AYUDHYA (KRUNGSRI)* 🏦\
            \n- *KASIKORNBANK* 🏦\
            \n\
            \n❗ Доступно при обмене от *1 000 THB*. Сумма в батах должна быть кратна 100.\
            \n\
            \nПодробную инструкцию по использованию вы можете скачать с помощью кнопки ниже ⬇️\
            ''',
    'eng' : '''
            \nThai ATMs allow you to withdraw cash remotely using a QR code. Today our service works with the following banks:\
            \n\
            \n- *BANGKOK BANK* 🏦\
            \n- *BANK OF AYUDHYA (KRUNGSRI)* 🏦\
            \n- *KASIKORNBANK* 🏦\
            \n\
            \n❗ Available for exchange from *1 000 THB*. The amount in baht must be a multiple of 100.\
            \n\
            \nYou can download detailed instructions by pressing the button below ⬇️\
            ''',
}

# message that displays when user wants to get details about airport delivery
AIRPORT_MESSAGE = {
    'rus' : '''
            \nМы поможем вам получить наличные баты *сразу по прилете* в Таиланд!\
            \n\
            \nЗакажите такси из аэропорта до места своего размещения, где вас уже будет ждать наш курьер с необходимой суммой.\
            \n\
            \nМы поможем оплатить ваше такси через qr код водителя, не переживайте за это.\
            \n\
            \n❗ Работаем на Пхукете. Доступно при обмене от *1 000 THB*.\
            ''',
    'eng' : '''
            \nWe will help you get cash baht *immediately upon arrival* in Thailand!\
            \n\
            \nOrder a taxi from the airport to your accommodation, where our courier will be waiting for you with the required amount.\
            \n\
            \nWe will help you pay for your taxi via the driver's qr code, don't worry about it.\
            \n\
            \n❗ We work in Phuket. Available for exchange from *1 000 THB*.\
            ''',
}

# message that displays when user wants to get details about delivery
DELIVERY_MESSAGE = {
    'rus' : '''
            \nПриедем и передадим наличные лично в руки: *удобно и безопасно*.\
            \n\
            \n❗ Работаем на Пхукете. Доступно при обмене от *1 000 THB*. Стоимость доставки - *500 THB*\
            ''',
    'eng' : '''
            \nWe will come and hand over the cash in person: *conveniently and safely*.\
            \n\
            \n❗ We work in Phuket. Available for exchange from *1 000 THB*. Delivery cost - *500 THB*\
            ''',
}

# message that displays when user wants to get details about transfer
TRANSFER_MESSAGE = {
    'rus' : '''
            \nПоможем вам оплатить *крупную покупку*, *бронирование отеля*, *авиабилетов* и многое другое. Рассчитываетесь с нами, получаете оплаченную услугу! *Удобно и просто*.\
            \n\
            \n❗ Доступно при оплате услуг от *1 000 THB*.\
            ''',
    'eng' : '''
            \nWe will help you pay for *large purchases*, *hotel reservations*, *flight tickets* and much more. Pay with us, get a paid service! *Convenient and simple*.\
            \n\
            \n❗ Available from *1 000 THB*.\
            ''',
}

# message that displays when user wants to know more about banks
BANKS_MESSAGE = {
    'rus' : '''
            \nВоспользоваться нашими услугами можно, выполнив перевод любым из удобных вам способов:\
            \n\
            \n- *РАЙФФАЙЗЕН БАНК* 🏦\
            \n- *ТИНЬКОФФ* 🏦\
            \n- *СБЕР* 🏦\
            \n- *СБП* 🏦\
            ''',
    'eng' : '''
             \nYou can use our services by translating in any of the ways convenient for you:\
             \n\
             \n- *RAIFFEISEN BANK* 🏦\
             \n- *TINKOFF* 🏦\
             \n- *SBER* 🏦\
             \n- *SBP* 🏦\
             ''',
}

# file id with instruction of using bangkok bank atm
BANGKOK_FILE = 'BQACAgIAAxkBAAPRZ1_2Nnfs-wUwl99DSXtq8O4q1GoAAqVmAAJoOvhKS6mBxQTxDvU2BA'

# file id with instruction of using kasikorn bank atm
KASIKORN_FILE ='BQACAgIAAxkBAAPQZ1_2H0bO4rjdC6TJXedh_2dnhDUAAqNmAAJoOvhKWNQBivv9Chg2BA'

# file id with instruction of using krungsri bank atm
KRUNGSRI_FILE = 'BQACAgUAAxkBAAOwZ1rAnLAeuLXiKvuVes0eg1UlTugAAlAJAALBlqBXhjscIoxxUjk2BA' # add !!!

# message to choose currency pair
PAIRS_MESSAGE = {
    'rus' : 'Выберите пару для обмена:',
    'eng' : 'Select a pair to exchange:',
}

# message to exchange type
EXCHANGE_TYPE_MESSAGE = {
    'rus' : 'Выберите удобный способ обмена:',
    'eng' : 'Select a convenient exchange method:',
}

# part of message that added when user gets the rate
ADDITIONAL_MESSAGE = {
    'rus' : '❗ Для совершения обмена подтвердите свою заявку с помощью кнопки ниже ⬇️',
    'eng' : '❗ To make an exchange, confirm your application using the button below ⬇️',
}

REVIEWS_MEDIA_IMAGES = [telebot.types.InputMediaPhoto(media='AgACAgIAAxkBAAMHZ1pt0PDdBPC_UdC_Kg5asN9cSNYAAorgMRveNMlKc5RTG8crSgMBAAMCAAN5AAM2BA'),
           telebot.types.InputMediaPhoto(media='AgACAgIAAxkBAAMHZ1pt0PDdBPC_UdC_Kg5asN9cSNYAAorgMRveNMlKc5RTG8crSgMBAAMCAAN5AAM2BA'),
           telebot.types.InputMediaPhoto(media='AgACAgIAAxkBAAMHZ1pt0PDdBPC_UdC_Kg5asN9cSNYAAorgMRveNMlKc5RTG8crSgMBAAMCAAN5AAM2BA'),
           ]

from config_local import *
