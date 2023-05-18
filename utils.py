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


def extract_referral_from_message(text):
    """Extracts referral from text."""

    regex = r'(?<=реферала )[a-zA-Z0-9]+'
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


def extract_exchange_info(text):
    """Extract exchange information from reply text."""

    regex = r'(?<=Пара: )[A-Z]+'
    currency = re.search(regex, text).group()

    regex = r'(?<=сумму в )[A-Z]+'
    amount_currency = re.search(regex, text).group()

    exchange_type = ''
    for key, value in config.TYPE_RUSSIAN.items():
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
