import os
from dotenv import load_dotenv
import telebot

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# manager's id (redirect users to him)
MANAGER_ID = '877069241' # change !!!

# manager's username
MANAGER_USERNAME = 'dyanashek' # change !!!

# director's id - gets all reports
DIRECTOR_ID = '877069241'

# bot's link
BOT_LINK = 'https://t.me/XChange_money_bot'

# bot's ID
BOT_ID = '6119183111'

TG_CHANNEL = 'https://t.me/Xchange_service'

INSTAGRAM = 'https://instagram.com/xchange_phuket'

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
    'kata' : 1.025,
    'ravai' : 1.025,
    'airport' : 1.025,
    'atm' : 1.022,
    'office' : 1.021,
    'transfer' : 1.02,
    'service' : 1.02,
}

# types of delivery and their minimal amount
TYPE_AMOUNT ={
    'delivery' : 40000,
    'kata' : 20000,
    'ravai' : 10000,
    'airport' : 40000,
    'atm' : 10000,
    'office' : 5000,
    'transfer' : 5000,
    'service' : 5000,
}

# types of delivery with translation
TYPE_RUSSIAN ={
    'delivery' : 'курьер (доставка)',
    'kata' : 'курьер (Ката)',
    'ravai' : 'курьер (Равай/Найхарн)',
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
            \n❗ Доступно при обмене от *10 000 THB*. Сумма в батах должна быть кратна 100.\
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
            \n❗ Available for exchange from *10,000 THB*. The amount in baht must be a multiple of 100.\
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
            \n❗ Работаем на Пхукете. Доступно при обмене от *40 000 THB*.\
            ''',
    'eng' : '''
            \nWe will help you get cash baht *immediately upon arrival* in Thailand!\
            \n\
            \nOrder a taxi from the airport to your accommodation, where our courier will be waiting for you with the required amount.\
            \n\
            \nWe will help you pay for your taxi via the driver's qr code, don't worry about it.\
            \n\
            \n❗ We work in Phuket. Available for exchange from *40 000 THB*.\
            ''',
}

# message that displays when user wants to get details about delivery
DELIVERY_MESSAGE = {
    'rus' : '''
            \nПриедем и передадим наличные лично в руки: *удобно и безопасно*.\
            \n\
            \n❗ Работаем на Пхукете. Доступно при обмене от *40 000 THB*.\
            \n- Для *района Ката* от *20 000 THB*.\
            \n- Для районов *Равай и Найхарн* от *10 000 THB*.\
            ''',
    'eng' : '''
            \nWe will come and hand over the cash in person: *conveniently and safely*.\
            \n\
            \n❗ We work in Phuket. Available for exchange from *40 000 THB*.\
            \n- For *Kata area* from *20 000 THB*.\
            \n- For districts *Rawai and Naiharn* from *10 000 THB*.\
            ''',
}

# message that displays when user wants to get details about transfer
TRANSFER_MESSAGE = {
    'rus' : '''
            \nПоможем вам оплатить *крупную покупку*, *бронирование отеля*, *авиабилетов* и многое другое. Рассчитываетесь с нами, получаете оплаченную услугу! *Удобно и просто*.\
            \n\
            \n❗ Доступно при оплате услуг от *5 000 THB*.\
            ''',
    'eng' : '''
            \nWe will help you pay for *large purchases*, *hotel reservations*, *flight tickets* and much more. Pay with us, get a paid service! *Convenient and simple*.\
            \n\
            \n❗ Available from *5,000 THB*.\
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
BANGKOK_FILE = 'BQACAgIAAxkBAAMFZGW71NNkl2IAAQPBHvb5TFOFzYexAALvMgACRbcpSxaDV9BMqOMDLwQ'

# file id with instruction of using kasikorn bank atm
KASIKORN_FILE ='BQACAgIAAxkBAAOdZHR9oREgNRyl9mWb2YScBpVoYAwAArMtAAJ1BKFLuErsmz0jrVIvBA'

# file id with instruction of using krungsri bank atm
KRUNGSRI_FILE = 'BQACAgIAAxkBAAOeZHR91PIeKmPE04ANaTdhOKjSc68AArgtAAJ1BKFLYIDcZj5vXjUvBA' # add !!!

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

REVIEWS_MEDIA_IMAGES = [telebot.types.InputMediaPhoto(media='AgACAgIAAxkBAAIBfmSKv3pCV2oW2xCg9NksPUHWjew5AAINzDEbBAdZSCGf28YBX6pPAQADAgADeQADLwQ'),
           telebot.types.InputMediaPhoto(media='AgACAgIAAxkBAAIBgGSKv39T_3g_9aMeg7y5X6MEC1HVAAIPzDEbBAdZSAYboa6bI67qAQADAgADeQADLwQ'),
           telebot.types.InputMediaPhoto(media='AgACAgIAAxkBAAIBgmSKv4QuSl2-duRzmg9g1F-P5YcZAAIQzDEbBAdZSFxwIxFg1k3MAQADAgADeQADLwQ'),
           ]