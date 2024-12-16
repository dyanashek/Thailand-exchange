import re

import config

def extract_referral(text, command):
    """Extracts referral from command."""
    referral = text.replace(f'{command}', '').replace(' ', '')

    regex = r'[^a-zA-Z0-9]'
    not_acceptable_symbols = re.search(regex, referral)

    if not_acceptable_symbols is not None:
        referral = ''

    return referral


def extract_referral_from_message(text, language):
    """Extracts referral from text."""

    if language == 'rus':
        regex = r'(?<=реферала )[a-zA-Z0-9]+'
    else:
        regex = r'(?<=To reserve a referral )[a-zA-Z0-9]+'

    referral = re.search(regex, text).group()

    return referral


def extract_amount_username(text):
    """Extract amount and username from command."""

    command_data = text.split(' ')

    if len(command_data) != 3:
        return False
    
    username = command_data[1].replace('@', '')

    try:
        amount = round(float(command_data[2].replace(',', '')), 2)
    except:
        return False
    
    return (username, amount)


def numbers_format(value):
    """Makes a good looking numbers format."""

    return '{:,}'.format(value).replace(',', ' ')


def extract_exchange_info(text, language):
    """Extract exchange information from reply text."""

    if language == 'rus':
        regex = r'(?<=Пара: )[A-Z]+'
    else:
        regex = r'(?<=Pair: )[A-Z]+'
    currency = re.search(regex, text).group()

    if language == 'rus':
        regex = r'(?<=сумму в )[A-Z]+'
    else:
        regex = r'(?<=amount in )[A-Z]+'

    amount_currency = re.search(regex, text).group()

    if language == 'rus':
        delivery_types = config.TYPE_RUSSIAN.items()
    else:
        delivery_types = config.TYPE_ENGLISH.items()

    exchange_type = ''
    for key, value in delivery_types:
        if value in text:
            exchange_type = key
            break
    
    return currency, exchange_type, amount_currency


def convert_to_float(text):
    try:
        amount = round(float(text.replace(' ', '').replace(',', '.')), 2)
    except:
        amount = False
    
    return amount

def escape_markdown(text):
    characters_to_escape = ['_', '*', '[', ']', '`']
    for char in characters_to_escape:
        text = text.replace(char, '\\' + char)

    return text


def validate_bonus(bonus):
    bonus = bonus.replace(',', '.')
    try:
        bonus = round(float(bonus), 2)
        if bonus < 1 and bonus > 0:
            return bonus
        else:
            return False
    except:
        return False
