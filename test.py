import qrcode
import io

import re
import requests
import config

def p2p_binance(currency = 'THB', amount = ''):
    """Gets price of buying or selling usdt on Binance p2p."""

    # indicate trade side
    side = 'BUY'
    if currency == 'THB':
        side = 'SELL'
    
    pay_types = []
    if currency == 'RUB':
        pay_types = config.BANKS

    # construct params
    data_binance = {
        "asset": config.COIN,
        "countries": [],
        "fiat": currency,
        "page": 1,
        "proMerchantAds": False,
        "publisherType": None,
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
        rub_price = p2p_binance(currency)
        
        rate = round(rub_price / thb_price, 3)

    elif currency == 'USD':
        usd_price = p2p_binance(currency)

        rate = round(thb_price / usd_price, 3)
    
    elif currency == 'USDT':

        rate = round(thb_price, 3)

    return rate

print(get_basic_exchange_rate('USD'), get_basic_exchange_rate('USDT'), get_basic_exchange_rate('RUB'))