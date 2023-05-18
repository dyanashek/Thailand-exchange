from telebot import types

import config

def send_referral_keyboard(referral):
    """Generates keyboards with options of sending links and QRs."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Получить ссылку и QR', callback_data = f'referral_info_{referral}'))
    keyboard.add(types.InlineKeyboardButton('Отменить', callback_data = f'cancel'))
    return keyboard

def reserve_referral_keyboard(referral):
    """Generates keyboards to confirm referral reservation."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Подтвердить', callback_data = f'referral_reserve_{referral}'))
    keyboard.add(types.InlineKeyboardButton('Отменить', callback_data = f'cancel'))
    return keyboard

def confirm_exchange_keyboard(referral, amount):
    """Generates keyboards to confirm exchange to increase referral's amount."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Подтвердить', callback_data = f'referral_increase_{referral}_{amount}'))
    keyboard.add(types.InlineKeyboardButton('Отменить', callback_data = f'cancel'))
    return keyboard

def confirm_reduce_all_keyboard():
    """Generates keyboards to confirm reducing all referrals balance to 0."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Подтвердить', callback_data = f'referral_reduce_all'))
    keyboard.add(types.InlineKeyboardButton('Отменить', callback_data = f'cancel'))
    return keyboard

def confirm_reduce_keyboard(referral):
    """Generates keyboards to confirm reducing referral's balance to 0."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Подтвердить', callback_data = f'referral_reduce_{referral}'))
    keyboard.add(types.InlineKeyboardButton('Отменить', callback_data = f'cancel'))
    return keyboard

def main_keyboard():
    """Generates main keyboard for navigation."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('💸 Калькулятор обмена', callback_data = 'calculate_main'))
    keyboard.add(types.InlineKeyboardButton('👨‍💻 Менеджер', url = f'https://t.me/{config.MANAGER_USERNAME}'))
    # reviews = types.InlineKeyboardButton('👍 Отзывы', callback_data = 'reviews')
    faq = types.InlineKeyboardButton('💥 Услуги', callback_data = 'faq')
    keyboard.add(faq) # reviews, 
    keyboard.add(types.InlineKeyboardButton('💎 Специальные предложения', callback_data = 'service'))
    return keyboard

def menu_keyboard():
    """Generates keyboard with menu button."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('🧭 Меню', callback_data = 'menu'))
    return keyboard

def service_keyboard():
    """Generates keyboard with menu button."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('👨‍💻 Менеджер', url = f'https://t.me/{config.MANAGER_USERNAME}'))
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = 'back_main'))
    return keyboard

def question_keyboard():
    """Generates keyboard with menu button."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('🏧 Выдача через банкомат', callback_data = 'atm'))
    keyboard.add(types.InlineKeyboardButton('🛬 Доставка в аэропорт', callback_data = 'airport'))
    keyboard.add(types.InlineKeyboardButton('🚚 Доставка курьером', callback_data = 'delivery'))
    keyboard.add(types.InlineKeyboardButton('🧾 Оплата услуг', callback_data = 'transfer'))
    keyboard.add(types.InlineKeyboardButton('🏦 Перевод средств', callback_data = 'banks'))
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = 'back_main'))
    return keyboard

def atm_keyboard(source):
    """Generates keyboard with banks names."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('🏦 Bangkok bank', callback_data = 'bangkok'))
    keyboard.add(types.InlineKeyboardButton('💳 Kasikorn', callback_data = 'kasikorn'))
    # keyboard.add(types.InlineKeyboardButton('🏧 Krungsri', callback_data = 'krungsri'))
    keyboard.add(types.InlineKeyboardButton('💸 Калькулятор обмена', callback_data = f'calculate_{source}'))
    keyboard.add(types.InlineKeyboardButton('🏠 Главное меню', callback_data = 'back_main'))
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = 'back_faq'))
    return keyboard

def back_faq_keyboard(source):
    """Generates keyboard with back to faq and main buttons."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('💸 Калькулятор обмена', callback_data = f'calculate_{source}'))
    keyboard.add(types.InlineKeyboardButton('🏠 Главное меню', callback_data = 'back_main'))
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = 'back_faq'))
    return keyboard

def back_atm_keyboard():
    """Generates keyboard with back to faq and main buttons. If you press - original message will not change."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('🏠 Главное меню', callback_data = 'back_leave_main'))
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = 'back_leave_atm'))
    return keyboard

def pairs_keyboard(destination):
    """Generates keyboard with currency pairs."""

    keyboard = types.InlineKeyboardMarkup()
    rub = types.InlineKeyboardButton('RUB/THB', callback_data = 'exchange_RUB')
    usdt = types.InlineKeyboardButton('USDT/THB', callback_data = 'exchange_USDT')
    # usd = types.InlineKeyboardButton('USD/THB', callback_data = 'exchange_USD')
    keyboard.add(rub, usdt) #usd
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = f'back_{destination}'))
    return keyboard

def exchange_type_keyboard(currency):
    """Generates keyboard with exchange types."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Курьер от 40 000 THB', callback_data = f'exchange_{currency}_delivery'))
    keyboard.add(types.InlineKeyboardButton('Аэропорт от 40 000 THB', callback_data = f'exchange_{currency}_airport'))
    keyboard.add(types.InlineKeyboardButton('Банкомат от 10 000 THB', callback_data = f'exchange_{currency}_atm'))
    # keyboard.add(types.InlineKeyboardButton('Офис от 5 000 THB', callback_data = f'exchange_{currency}_office'))
    keyboard.add(types.InlineKeyboardButton('На тайский счет от 5 000 THB', callback_data = f'exchange_{currency}_transfer'))
    keyboard.add(types.InlineKeyboardButton('Оплата услуг от 5 000 THB', callback_data = f'exchange_{currency}_service'))
    keyboard.add(types.InlineKeyboardButton('🏠 Главное меню', callback_data = 'back_main'))
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = 'back_pairs'))
    return keyboard

def amount_currency_keyboard(currency, exchange_type):
    """Generates keyboard with exchange types."""

    keyboard = types.InlineKeyboardMarkup()
    curr = types.InlineKeyboardButton(f'{currency}', callback_data = f'exchange_{currency}_{exchange_type}_{currency}')
    thb = types.InlineKeyboardButton('THB', callback_data = f'exchange_{currency}_{exchange_type}_THB')
    keyboard.add(curr, thb)
    keyboard.add(types.InlineKeyboardButton('🏠 Главное меню', callback_data = 'back_main'))
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = f'back_type_{currency}'))
    return keyboard


def exchanged_keyboard(currency, exchange_type):
    """Generates keyboard with menu button and manager button."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('✅ Отправить заявку', callback_data = 'send'))
    keyboard.add(types.InlineKeyboardButton('🔄 Ввести другую сумму', callback_data = f'recalculate_{currency}_{exchange_type}'))
    keyboard.add(types.InlineKeyboardButton('🧭 Меню', callback_data = f'exchanged_{currency}_{exchange_type}'))
    return keyboard

def manager_keyboard():
    """Generates keyboard with manager button."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('👨‍💻 Менеджер', url = f'https://t.me/{config.MANAGER_USERNAME}'))
    keyboard.add(types.InlineKeyboardButton('🧭 Меню', callback_data = 'sended'))
    return keyboard

def manager_application_keyboard(currency, exchange_type):
    """Generates keyboard with manager button and send application button."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('✅ Отправить заявку', callback_data = 'send'))
    keyboard.add(types.InlineKeyboardButton('🔄 Ввести другую сумму', callback_data = f'recalculate_{currency}_{exchange_type}'))
    return keyboard

def only_manager_keyboard():
    """Generates keyboard with manager button."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('👨‍💻 Менеджер', url = f'https://t.me/{config.MANAGER_USERNAME}'))
    return keyboard