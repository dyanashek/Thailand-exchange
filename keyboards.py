from telebot import types

import config

def send_referral_keyboard(referral, lang):
    """Generates keyboards with options of sending links and QRs."""

    keyboard = types.InlineKeyboardMarkup()

    if lang == 'rus':
        keyboard.add(types.InlineKeyboardButton('Получить ссылку и QR', callback_data = f'referral_rus_info_{referral}'))
        keyboard.add(types.InlineKeyboardButton('Отменить', callback_data = f'cancel_rus'))

    else:
        keyboard.add(types.InlineKeyboardButton('Get link and QR', callback_data = f'referral_eng_info_{referral}'))
        keyboard.add(types.InlineKeyboardButton('Cancel', callback_data = f'cancel_eng'))

    return keyboard

def reserve_referral_keyboard(referral, lang):
    """Generates keyboards to confirm referral reservation."""

    keyboard = types.InlineKeyboardMarkup()

    if lang == 'rus':
        keyboard.add(types.InlineKeyboardButton('Подтвердить', callback_data = f'referral_rus_reserve_{referral}'))
        keyboard.add(types.InlineKeyboardButton('Отменить', callback_data = f'cancel_rus'))
    else:
        keyboard.add(types.InlineKeyboardButton('Confirm', callback_data = f'referral_eng_reserve_{referral}'))
        keyboard.add(types.InlineKeyboardButton('Cancel', callback_data = f'cancel_eng'))

    return keyboard

def confirm_exchange_keyboard(referral, amount, lang):
    """Generates keyboards to confirm exchange to increase referral's amount."""

    keyboard = types.InlineKeyboardMarkup()

    if lang == 'rus':
        keyboard.add(types.InlineKeyboardButton('Подтвердить', callback_data = f'referral_rus_increase_{referral}_{amount}'))
        keyboard.add(types.InlineKeyboardButton('Отменить', callback_data = f'cancel_rus'))
    
    else:
        keyboard.add(types.InlineKeyboardButton('Confirm', callback_data = f'referral_eng_increase_{referral}_{amount}'))
        keyboard.add(types.InlineKeyboardButton('Cancel', callback_data = f'cancel_eng'))

    return keyboard

def confirm_reduce_all_keyboard(lang):
    """Generates keyboards to confirm reducing all referrals balance to 0."""

    keyboard = types.InlineKeyboardMarkup()
    
    if lang == 'rus':
        keyboard.add(types.InlineKeyboardButton('Подтвердить', callback_data = f'referral_rus_reduce_all'))
        keyboard.add(types.InlineKeyboardButton('Отменить', callback_data = f'cancel_rus'))
    else:
        keyboard.add(types.InlineKeyboardButton('Confirm', callback_data = f'referral_eng_reduce_all'))
        keyboard.add(types.InlineKeyboardButton('Cancel', callback_data = f'cancel_eng'))

    return keyboard

def confirm_reduce_keyboard(referral, lang):
    """Generates keyboards to confirm reducing referral's balance to 0."""

    keyboard = types.InlineKeyboardMarkup()

    if lang == 'rus':
        keyboard.add(types.InlineKeyboardButton('Подтвердить', callback_data = f'referral_rus_reduce_{referral}'))
        keyboard.add(types.InlineKeyboardButton('Отменить', callback_data = f'cancel_rus'))
    else:
        keyboard.add(types.InlineKeyboardButton('Confirm', callback_data = f'referral_eng_reduce_{referral}'))
        keyboard.add(types.InlineKeyboardButton('Cancel', callback_data = f'cancel_eng'))

    return keyboard

def main_keyboard(lang):
    """Generates main keyboard for navigation."""

    keyboard = types.InlineKeyboardMarkup()

    if lang == 'rus':
        keyboard.add(types.InlineKeyboardButton('💸 Калькулятор обмена', callback_data = 'calculate_rus_main'))
        keyboard.add(types.InlineKeyboardButton('👨‍💻 Менеджер', url = f'https://t.me/{config.MANAGER_USERNAME}'))
        reviews = types.InlineKeyboardButton('👍 Отзывы', callback_data = 'reviews_rus')
        leave_review = types.InlineKeyboardButton('🖋 Оставить отзыв', url = config.TG_CHANNEL)
        keyboard.add(reviews, leave_review)
        keyboard.add(types.InlineKeyboardButton('🏦 Перевод средств', callback_data = 'banks_rus'))
        keyboard.add(types.InlineKeyboardButton('💥 Подробнее об услугах', callback_data = 'faq_rus')) # reviews, 
        keyboard.add(types.InlineKeyboardButton('💎 Специальные предложения', callback_data = 'service_rus'))
        keyboard.add(types.InlineKeyboardButton('📸 Наш Instagram', url = config.INSTAGRAM))
        keyboard.add(types.InlineKeyboardButton('🔁 Change language', callback_data = 'language_change'))

    else:
        keyboard.add(types.InlineKeyboardButton('💸 Exchange calculator', callback_data = 'calculate_eng_main'))
        keyboard.add(types.InlineKeyboardButton('👨‍💻 Manager', url = f'https://t.me/{config.MANAGER_USERNAME}'))
        reviews = types.InlineKeyboardButton('👍 Reviews', callback_data = 'reviews_eng')
        leave_review = types.InlineKeyboardButton('🖋 Leave feedback', url = config.TG_CHANNEL)
        keyboard.add(reviews, leave_review)
        keyboard.add(types.InlineKeyboardButton('🏦 Money transaction', callback_data = 'banks_eng'))
        keyboard.add(types.InlineKeyboardButton('💥 More about services', callback_data = 'faq_eng'))
        keyboard.add(types.InlineKeyboardButton('💎 Special offers', callback_data = 'service_eng'))
        keyboard.add(types.InlineKeyboardButton('📸 Our Instagram', url = config.INSTAGRAM))
        keyboard.add(types.InlineKeyboardButton('🔁 Изменить язык', callback_data = 'language_change'))

    return keyboard

def menu_keyboard(lang):
    """Generates keyboard with menu button."""

    keyboard = types.InlineKeyboardMarkup()
    if lang == 'rus':
        keyboard.add(types.InlineKeyboardButton('🧭 Меню', callback_data = 'menu_rus'))
    else:
        keyboard.add(types.InlineKeyboardButton('🧭 Menu', callback_data = 'menu_eng'))

    return keyboard

def service_keyboard(lang):
    """Generates keyboard with menu button."""

    keyboard = types.InlineKeyboardMarkup()

    if lang == 'rus':
        keyboard.add(types.InlineKeyboardButton('👨‍💻 Менеджер', url = f'https://t.me/{config.MANAGER_USERNAME}'))
        keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = 'back_rus_main'))
    else:
        keyboard.add(types.InlineKeyboardButton('👨‍💻 Manager', url = f'https://t.me/{config.MANAGER_USERNAME}'))
        keyboard.add(types.InlineKeyboardButton('⬅️ Back', callback_data = 'back_eng_main'))

    return keyboard

def question_keyboard(lang):
    """Generates keyboard with menu button."""

    keyboard = types.InlineKeyboardMarkup()

    if lang == 'rus':
        keyboard.add(types.InlineKeyboardButton('🏧 Выдача через банкомат', callback_data = 'atm_rus'))
        keyboard.add(types.InlineKeyboardButton('🛬 Доставка в аэропорт', callback_data = 'airport_rus'))
        keyboard.add(types.InlineKeyboardButton('🚚 Доставка курьером', callback_data = 'delivery_rus'))
        keyboard.add(types.InlineKeyboardButton('🧾 Оплата услуг', callback_data = 'transfer_rus'))
        keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = 'back_rus_main'))
    
    else:
        keyboard.add(types.InlineKeyboardButton('🏧 Withdrawal via ATM', callback_data = 'atm_eng'))
        keyboard.add(types.InlineKeyboardButton('🛬 Delivery to the airport', callback_data = 'airport_eng'))
        keyboard.add(types.InlineKeyboardButton('🚚 Courier delivery', callback_data = 'delivery_eng'))
        keyboard.add(types.InlineKeyboardButton('🧾 Payment for services', callback_data = 'transfer_eng'))
        keyboard.add(types.InlineKeyboardButton('⬅️ Back', callback_data = 'back_eng_main'))

    return keyboard

def atm_keyboard(source, lang):
    """Generates keyboard with banks names."""

    keyboard = types.InlineKeyboardMarkup()

    if lang == 'rus':
        keyboard.add(types.InlineKeyboardButton('🏦 Bangkok bank', callback_data = 'bangkok_rus'))
        keyboard.add(types.InlineKeyboardButton('💳 Kasikorn', callback_data = 'kasikorn_rus'))
        keyboard.add(types.InlineKeyboardButton('🏧 Krungsri', callback_data = 'krungsri_rus'))
        keyboard.add(types.InlineKeyboardButton('💸 Калькулятор обмена', callback_data = f'calculate_rus_{source}'))
        keyboard.add(types.InlineKeyboardButton('🏠 Главное меню', callback_data = 'back_rus_main'))
        keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = 'back_rus_faq'))
    else:
        keyboard.add(types.InlineKeyboardButton('🏦 Bangkok bank', callback_data = 'bangkok_eng'))
        keyboard.add(types.InlineKeyboardButton('💳 Kasikorn', callback_data = 'kasikorn_eng'))
        keyboard.add(types.InlineKeyboardButton('🏧 Krungsri', callback_data = 'krungsri_eng'))
        keyboard.add(types.InlineKeyboardButton('💸 Exchange calculator', callback_data = f'calculate_eng_{source}'))
        keyboard.add(types.InlineKeyboardButton('🏠 Main menu', callback_data = 'back_eng_main'))
        keyboard.add(types.InlineKeyboardButton('⬅️ Back', callback_data = 'back_eng_faq'))

    return keyboard

def back_faq_keyboard(source, lang):
    """Generates keyboard with back to faq and main buttons."""

    keyboard = types.InlineKeyboardMarkup()

    if lang == 'rus':
        keyboard.add(types.InlineKeyboardButton('💸 Калькулятор обмена', callback_data = f'calculate_rus_{source}'))
        keyboard.add(types.InlineKeyboardButton('🏠 Главное меню', callback_data = 'back_rus_main'))
        keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = 'back_rus_faq'))
    else:
        keyboard.add(types.InlineKeyboardButton('💸 Exchange calculator', callback_data = f'calculate_eng_{source}'))
        keyboard.add(types.InlineKeyboardButton('🏠 Main menu', callback_data = 'back_eng_main'))
        keyboard.add(types.InlineKeyboardButton('⬅️ Back', callback_data = 'back_eng_faq'))

    return keyboard

def back_atm_keyboard(lang):
    """Generates keyboard with back to faq and main buttons. If you press - original message will not change."""

    keyboard = types.InlineKeyboardMarkup()

    if lang == 'rus':
        keyboard.add(types.InlineKeyboardButton('🏠 Главное меню', callback_data = 'back_rus_leave_main'))
        keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = 'back_rus_leave_atm'))
    else:
        keyboard.add(types.InlineKeyboardButton('🏠 Main menu', callback_data = 'back_eng_leave_main'))
        keyboard.add(types.InlineKeyboardButton('⬅️ Back', callback_data = 'back_eng_leave_atm'))

    return keyboard

def pairs_keyboard(destination, lang):
    """Generates keyboard with currency pairs."""

    keyboard = types.InlineKeyboardMarkup()

    if lang == 'rus':
        rub = types.InlineKeyboardButton('RUB/THB', callback_data = 'exchange_rus_RUB')
        usdt = types.InlineKeyboardButton('USDT/THB', callback_data = 'exchange_rus_USDT')
        # usd = types.InlineKeyboardButton('USD/THB', callback_data = 'exchange_rus_USD')
        keyboard.add(rub, usdt) #usd
        keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = f'back_rus_{destination}'))
    
    else:
        rub = types.InlineKeyboardButton('RUB/THB', callback_data = 'exchange_eng_RUB')
        usdt = types.InlineKeyboardButton('USDT/THB', callback_data = 'exchange_eng_USDT')
        # usd = types.InlineKeyboardButton('USD/THB', callback_data = 'exchange_eng_USD')
        keyboard.add(rub, usdt) #usd
        keyboard.add(types.InlineKeyboardButton('⬅️ Back', callback_data = f'back_eng_{destination}'))

    return keyboard

def exchange_type_keyboard(currency, lang):
    """Generates keyboard with exchange types."""

    keyboard = types.InlineKeyboardMarkup()

    if lang == 'rus':
        keyboard.add(types.InlineKeyboardButton('Курьер (в зависимости от района)', callback_data = f'exchange_rus_{currency}_choose'))
        keyboard.add(types.InlineKeyboardButton('Аэропорт от 40 000 THB', callback_data = f'exchange_rus_{currency}_airport'))
        keyboard.add(types.InlineKeyboardButton('Банкомат от 10 000 THB', callback_data = f'exchange_rus_{currency}_atm'))
        # keyboard.add(types.InlineKeyboardButton('Офис от 5 000 THB', callback_data = f'exchange_rus_{currency}_office'))
        keyboard.add(types.InlineKeyboardButton('На тайский счет от 5 000 THB', callback_data = f'exchange_rus_{currency}_transfer'))
        keyboard.add(types.InlineKeyboardButton('Оплата услуг от 5 000 THB', callback_data = f'exchange_rus_{currency}_service'))
        keyboard.add(types.InlineKeyboardButton('🏠 Главное меню', callback_data = 'back_rus_main'))
        keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = 'back_rus_pairs'))

    else:
        keyboard.add(types.InlineKeyboardButton('Courier (depending on area)', callback_data = f'exchange_eng_{currency}_choose'))
        keyboard.add(types.InlineKeyboardButton('Airport from 40 000 THB', callback_data = f'exchange_eng_{currency}_airport'))
        keyboard.add(types.InlineKeyboardButton('ATM from 10 000 THB', callback_data = f'exchange_eng_{currency}_atm'))
        # keyboard.add(types.InlineKeyboardButton('Офис от 5 000 THB', callback_data = f'exchange_eng_{currency}_office'))
        keyboard.add(types.InlineKeyboardButton('Thai account from 5 000 THB', callback_data = f'exchange_eng_{currency}_transfer'))
        keyboard.add(types.InlineKeyboardButton('Services from 5 000 THB', callback_data = f'exchange_eng_{currency}_service'))
        keyboard.add(types.InlineKeyboardButton('🏠 Main menu', callback_data = 'back_eng_main'))
        keyboard.add(types.InlineKeyboardButton('⬅️ Back', callback_data = 'back_eng_pairs'))

    return keyboard

def amount_currency_keyboard(currency, exchange_type, lang):
    """Generates keyboard with exchange types."""

    keyboard = types.InlineKeyboardMarkup()

    if lang == 'rus':
        curr = types.InlineKeyboardButton(f'{currency}', callback_data = f'exchange_rus_{currency}_{exchange_type}_{currency}')
        thb = types.InlineKeyboardButton('THB', callback_data = f'exchange_rus_{currency}_{exchange_type}_THB')
        keyboard.add(curr, thb)
        keyboard.add(types.InlineKeyboardButton('🏠 Главное меню', callback_data = 'back_rus_main'))
        keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = f'back_rus_type_{currency}'))
    
    else:
        curr = types.InlineKeyboardButton(f'{currency}', callback_data = f'exchange_eng_{currency}_{exchange_type}_{currency}')
        thb = types.InlineKeyboardButton('THB', callback_data = f'exchange_eng_{currency}_{exchange_type}_THB')
        keyboard.add(curr, thb)
        keyboard.add(types.InlineKeyboardButton('🏠 Main menu', callback_data = 'back_eng_main'))
        keyboard.add(types.InlineKeyboardButton('⬅️ Back', callback_data = f'back_eng_type_{currency}'))

    return keyboard


def exchanged_keyboard(currency, exchange_type, lang):
    """Generates keyboard with menu button and manager button."""

    keyboard = types.InlineKeyboardMarkup()

    if lang == 'rus':
        keyboard.add(types.InlineKeyboardButton('✅ Отправить заявку', callback_data = 'send_rus'))
        keyboard.add(types.InlineKeyboardButton('🔄 Ввести другую сумму', callback_data = f'recalculate_rus_{currency}_{exchange_type}'))
        keyboard.add(types.InlineKeyboardButton('🧭 Меню', callback_data = f'exchanged_rus_{currency}_{exchange_type}'))
    else:
        keyboard.add(types.InlineKeyboardButton('✅ Submit a request', callback_data = 'send_eng'))
        keyboard.add(types.InlineKeyboardButton('🔄 Enter another amount', callback_data = f'recalculate_eng_{currency}_{exchange_type}'))
        keyboard.add(types.InlineKeyboardButton('🧭 Menu', callback_data = f'exchanged_eng_{currency}_{exchange_type}'))

    return keyboard

def manager_keyboard(lang):
    """Generates keyboard with manager button."""

    keyboard = types.InlineKeyboardMarkup()

    if lang == 'rus':
        keyboard.add(types.InlineKeyboardButton('👨‍💻 Менеджер', url = f'https://t.me/{config.MANAGER_USERNAME}'))
        keyboard.add(types.InlineKeyboardButton('🧭 Меню', callback_data = 'sended_rus'))
    else:
        keyboard.add(types.InlineKeyboardButton('👨‍💻 Manager', url = f'https://t.me/{config.MANAGER_USERNAME}'))
        keyboard.add(types.InlineKeyboardButton('🧭 Menu', callback_data = 'sended_eng'))
    
    return keyboard

def manager_application_keyboard(currency, exchange_type, lang):
    """Generates keyboard with manager button and send application button."""

    keyboard = types.InlineKeyboardMarkup()

    if lang == 'rus':
        keyboard.add(types.InlineKeyboardButton('✅ Отправить заявку', callback_data = 'send_rus'))
        keyboard.add(types.InlineKeyboardButton('🔄 Ввести другую сумму', callback_data = f'recalculate_rus_{currency}_{exchange_type}'))
    else:
        keyboard.add(types.InlineKeyboardButton('✅ Submit a request', callback_data = 'send_eng'))
        keyboard.add(types.InlineKeyboardButton('🔄 Enter another amount', callback_data = f'recalculate_eng_{currency}_{exchange_type}'))
    
    return keyboard


def only_manager_keyboard(lang):
    """Generates keyboard with manager button."""

    keyboard = types.InlineKeyboardMarkup()
    if lang == 'rus':
        keyboard.add(types.InlineKeyboardButton('👨‍💻 Менеджер', url = f'https://t.me/{config.MANAGER_USERNAME}'))
    else:
        keyboard.add(types.InlineKeyboardButton('👨‍💻 Manager', url = f'https://t.me/{config.MANAGER_USERNAME}'))

    return keyboard


def only_back_keyboard(lang):
    keyboard = types.InlineKeyboardMarkup()

    if lang == 'rus':
        keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = 'back_rus_main'))
    else:
        keyboard.add(types.InlineKeyboardButton('⬅️ Back', callback_data = 'back_eng_main'))

    return keyboard


def delivery_types_keyboard(currency, lang):
    keyboard = types.InlineKeyboardMarkup()

    if lang == 'rus':
        keyboard.add(types.InlineKeyboardButton('Пхукет от 40 000 THB', callback_data = f'exchange_rus_{currency}_delivery'))
        keyboard.add(types.InlineKeyboardButton('📍 Ката от 20 000 THB', callback_data = f'exchange_rus_{currency}_kata'))
        keyboard.add(types.InlineKeyboardButton('📍 Равай/Найхарн  от 10 000 THB', callback_data = f'exchange_rus_{currency}_ravai'))
        keyboard.add(types.InlineKeyboardButton('🏠 Главное меню', callback_data = 'back_rus_main'))
        keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = f'back_rus_type_{currency}'))
    else:
        keyboard.add(types.InlineKeyboardButton('Phoket from 40 000 THB', callback_data = f'exchange_eng_{currency}_delivery'))
        keyboard.add(types.InlineKeyboardButton('📍 Kata from 20 000 THB', callback_data = f'exchange_eng_{currency}_kata'))
        keyboard.add(types.InlineKeyboardButton('📍 Rawai/NaiHarn  from 10 000 THB', callback_data = f'exchange_eng_{currency}_ravai'))
        keyboard.add(types.InlineKeyboardButton('🏠 Main menu', callback_data = 'back_eng_main'))
        keyboard.add(types.InlineKeyboardButton('⬅️ Back', callback_data = f'back_eng_type_{currency}'))

    return keyboard

def languages_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    
    keyboard.add(types.InlineKeyboardButton('Русский', callback_data = f'language_rus_second'))
    keyboard.add(types.InlineKeyboardButton('English', callback_data = f'language_eng_second'))

    return keyboard


def languages_first_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    
    keyboard.add(types.InlineKeyboardButton('Русский', callback_data = f'language_rus_first'))
    keyboard.add(types.InlineKeyboardButton('English', callback_data = f'language_eng_first'))

    return keyboard