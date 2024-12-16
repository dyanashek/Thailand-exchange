import datetime

import utils
import config

OUTDATED = {
    'rus' : 'Данные устарели, перейдите в меню и попробуйте снова.',
    'eng' : 'Data outdated, proceed to the main menu and try again.',
}

OUTDATED_RATE = {
    'rus' : 'Данные по курсу устарели, перейдите в меню и попробуйте снова.',
    'eng' : 'Exchange rate data has been outdated, proceed to the main menu and try again.',
}

TRANSFER_DECLINED = {
    'rus' : 'Обмен валюты отменен.',
    'eng' : 'Currency exchange has been canceled.',
}

SEND_SLIP = {
    'rus' : 'Отправьте скриншот, подтверждающий совершение перевода.\nВоспользуйтесь командой */cancel_transfer*, если не совершали перевод.',
    'eng' : 'Send a screenshot confirming the transfer.\nUse the */cancel_transfer* command if you have not made a transfer.',
}

NO_CURRENT_TRANSFER = {
    'rus' : 'Не ожидается ввода информации.',
    'eng' : 'No input awaiting.',
}

CHECK_TRANSFER = {
    'rus' : 'Ваш платеж *ожидает подтверждения* администратором, мы пришлем уведомление.',
    'eng' : 'Your payment is *awaiting confirmation* by the administrator, we will send a notification.',
}

ADMIN_OUTDATED = 'Данные устарели.'

ADMIN_RECEIVED = 'Платеж подтвержден.'

ADMIN_NO_RECEIVE = 'Платеж не подтвержден.'

TRANSFER_DECLINED_BY_ADMIN = {
    'rus' : 'Ваш платеж *не подтвержден* администратором, свяжитесь с нами, если возникли вопросы.',
    'eng' : 'Your payment is *not confirmed* by the administrator, please contact us if you have any questions.',
}

TRANSFER_CONFIRMED_BY_ADMIN = {
    'rus' : 'Ваш платеж *подтвержден* администратором, найдите банкомат *Bangkok Bank* и подтвердите, когда будете возле него.',
    'eng' : 'Your payment is *confirmed* by the administrator, find a *Bangkok Bank* ATM and confirm when you get there.',
}

NEAR_ATM = {
    'rus' : 'Администратору *отправлено уведомление* о том, что вы находитесь у банкомата - в ближайшее время мы *пришлем уведомление*, подтверждающее готовность к выдаче наличных средств.',
    'eng' : 'A notification has been sent to the administrator that you are at the ATM - we will soon send a notification confirming the readiness for dispensing cash.',
}

ADMIN_WAITING_QR = 'Ожидаем QR-код от клиента.'

QR_SENDED = {
    'rus' : "QR-код *отправлен* администратору, нажмите 'confirm' на экране банкомата, когда получите соответствующее уведомление.",
    'eng' : "QR code *sent* to administrator, press 'confirm' on ATM screen when prompted.",
}

ADMIN_ASKED_REENTER = 'Запрошена повторная отправка QR-кода.'

ADMIN_SUCCESS = 'Обмен помечен как успешный.'

ADMIN_FAILED = 'Обмен помечен как неуспешный.'

AMOUNT_RULES = {
    'rus' : f"🚫 Для того, чтобы воспользоваться данной услугой сумма к обмену должна быть кратна 100 и не должна превышать {utils.numbers_format(config.MAX_AMOUNT)} THB.",
    'eng' : f"🚫 In order to use this service, the amount to be exchanged must be a multiple of 100 and must not exceed {utils.numbers_format(config.MAX_AMOUNT)} THB.",
}

TIME_RULES = {
    'rus' : '🚫 Вы можете воспользоваться данной услугой в период с 10 до 20 местного времени. Для совершения обмена воспользуйтесь кнопкой "отправить заявку".',
    'eng' : '🚫 You can use this service from 10 to 20 local time. Use the "submit a request" button to proceed the exchange.',
}

def confirm_payment(language, exchange_id, user_id, amount_currency, currency, amount_thb, status, rate_time):
    if language == 'rus':
        if currency == 'USDT':
            reply_text = f'''
                        \nДля получения {utils.numbers_format(amount_thb)} THB через банкомат - совершите перевод по следующим реквизитам:\
                        \n\
                        \n*Сумма:* {utils.numbers_format(amount_currency)} USDT\
                        \n*Адрес кошелька:* {config.CRYPTO_WALLET}\
                        \n*Сеть:* TRC20\
                        \n\
                        \n*ВАЖНО:* после того, как вы увидели это сообщение - у вас есть 15 минут на совершение перевода, далее фактический курс может отличаться.\
                        \nПосле оплаты нажмите *"Подтвердить"*.\
                        '''

        elif currency == 'RUB':
            bank = config.BANK
            card = config.ACCOUNT
            number = config.NUMBER
            receiver = config.RECEIVER

            reply_text = f'''
                        \nДля получения {utils.numbers_format(amount_thb)} THB через банкомат - совершите перевод по следующим реквизитам:\
                        \n\
                        \n*Сумма:* {utils.numbers_format(amount_currency)} RUB\
                        \n*Банк:* {bank}\
                        \n*Номер карты:* {card}\
                        \n*Номер телефона:* {number}\
                        \n*Получатель:* {receiver}\
                        \n*Комментарий к платежу:* {1000 + exchange_id}\
                        \n\
                        \n*ВАЖНО:* отсутствие комментария приведет к отмене сделки; после того, как вы увидели это сообщение - у вас есть 15 минут на совершение перевода, далее фактический курс может отличаться.\
                        \nПосле оплаты нажмите *"Подтвердить"*.\
                        '''

    elif language == 'eng':
        if currency == 'USDT':
            reply_text = f'''
                         \nTo receive {utils.numbers_format(amount_thb)} THB through an ATM, make a transfer using the following details:\
                         \n\
                         \n*Amount:* {utils.numbers_format(amount_currency)} USDT\
                         \n*Wallet address:* {config.CRYPTO_WALLET}\
                         \n*Network:* TRC20\
                         \n\
                         \n*IMPORTANT:* after you have seen this message, you have 15 minutes to complete the transfer, then the actual rate may differ.\
                         \nAfter payment, click *"Confirm"*.\
                         '''

        elif currency == 'RUB':
            bank = config.BANK
            card = config.ACCOUNT
            number = config.NUMBER
            receiver = config.RECEIVER

            reply_text = f'''
                         \nTo receive {utils.numbers_format(amount_thb)} THB through an ATM, make a transfer using the following details:\
                         \n\
                         \n*Amount:* {utils.numbers_format(amount_currency)} RUB\
                         \n*Bank:* {bank}\
                         \n*Card number:* {card}\
                         \n*Phone number:* {number}\
                         \n*Receiver:* {receiver}\
                         \n*Payment comment:* {1000 + exchange_id}\
                         \n\
                         \n*IMPORTANT:* transfers without comment will result in the exchange being cancelled; after you have seen this message, you have 15 minutes to complete the transfer, then the actual rate may differ.\
                         \nAfter payment, click *"Confirm"*.\
                         '''
    
    return reply_text


def confirm_receive(exchange_id, username, user_id, amount_currency, currency, amount_thb, status, rate_time):
    if username and username != 'None':
        username = utils.escape_markdown(username)
    else:
        username = 'не указано'

    rate_time_text = rate_time.strftime("%d.%m.%Y %H:%M")
    if (datetime.datetime.utcnow() + datetime.timedelta(hours=7)) - datetime.timedelta(minutes=25) > rate_time:
        rate_time_text += ' (проверьте актуальность курса)'

    reply_text = f'''
                \nПользователь @{username} пометил, что совершил перевод:\
                \n\
                \n*{utils.numbers_format(amount_currency)} {currency}* ⏩ {utils.numbers_format(amount_thb)} THB\
                \n*Время расчета курса:* {rate_time_text}\
                \n*ID обмена:* {1000 + exchange_id}\
                '''

    return reply_text


def confirm_ready(exchange_id, username, user_id, amount_currency, currency, amount_thb, status, rate_time):
    if username and username != 'None':
        username = utils.escape_markdown(username)
    else:
        username = 'не указано'

    reply_text = f'''
                \nПользователь @{username} пометил, что находится у банкомата:\
                \n\
                \n*{utils.numbers_format(amount_currency)} {currency}* ⏩ *{utils.numbers_format(amount_thb)} THB*\
                \n*ID обмена:* {1000 + exchange_id}\
                \n\
                \nПодтвердите готовность.\
                '''
    
    return reply_text


def send_qr(language, exchange_id, user_id, amount_currency, currency, amount_thb, status, rate_time):
    if language == 'rus':
        reply_text = f'''
                    \nДля получения наличных по обмену:\
                    \n*{utils.numbers_format(amount_currency)} {currency}* ⏩ *{utils.numbers_format(amount_thb)} THB*\
                    \n\
                    \nОтправьте в чат фото QR-кода с банкомата Bangkok Bank:\
                    \nДля этого нажмите кнопку "Cardless", если время снятия заканчивается нажмите *"Yes"*.\
                    '''

    elif language == 'eng':
        reply_text = f'''
                     \nTo receive cash by exchange:\
                     \n*{utils.numbers_format(amount_currency)} {currency}* ⏩ *{utils.numbers_format(amount_thb)} THB*\
                     \n\
                     \nSend a photo of the QR code from the Bangkok Bank ATM to chat:\
                     \nTo do this, click the "Cardless" button, if the withdrawal time is running out, click *"Yes"*.\
                     '''
    
    return reply_text


def confirm_cash(exchange_id, username, user_id, amount_currency, currency, amount_thb, status, rate_time):
    if username and username != 'None':
        username = utils.escape_markdown(username)
    else:
        username = 'не указано'

    reply_text = f'''
                \nПользователь @{username} отправил QR-код:\
                \n\
                \n*{utils.numbers_format(amount_currency)} {currency}* ⏩ *{utils.numbers_format(amount_thb)} THB*\
                \n*ID обмена:* {1000 + exchange_id}\
                \n\
                \nПодтвердите перевод.\
                '''
    
    return reply_text


def resend_qr(language, user_id, amount_currency, currency, amount_thb, status, rate_time):
    if language == 'rus':
        reply_text = f'''
                    \nЧто-то пошло не так\
                    \nДля получения наличных по обмену:\
                    \n*{utils.numbers_format(amount_currency)} {currency}* ⏩ *{utils.numbers_format(amount_thb)} THB*\
                    \n\
                    \nПовторно отправьте в чат фото другого QR-кода с банкомата Bangkok Bank:\
                    \nДля этого нажмите кнопку "Cardless", если время снятия заканчивается нажмите *"Yes"*.\
                    '''

    elif language == 'eng':
        reply_text = f'''
                     \nSomething went wrong\
                     \nTo receive cash by exchange:\
                     \n*{utils.numbers_format(amount_currency)} {currency}* ⏩ *{utils.numbers_format(amount_thb)} THB*\
                     \n\
                     \nSend a photo of another QR code from the Bangkok Bank ATM to chat once again:\
                     \nTo do this, click the "Cardless" button, if the withdrawal time is running out, click *"Yes"*.\
                     '''
    
    return reply_text


def confirm_status(exchange_id, username, user_id, amount_currency, currency, amount_thb, status, rate_time):
    if username and username != 'None':
        username = utils.escape_markdown(username)
    else:
        username = 'не указано'

    reply_text = f'''
                \nОбмен пользователя @{username}:\
                \n\
                \n*{utils.numbers_format(amount_currency)} {currency}* ⏩ *{utils.numbers_format(amount_thb)} THB*\
                \n*ID обмена:* {1000 + exchange_id}\
                \n\
                \nПрошел успешно?\
                '''
    
    return reply_text


def press_confirm(language, user_id, amount_currency, currency, amount_thb, status, rate_time):
    if language == 'rus':
        reply_text = f'''
                    \nНажмите *"confirm"* на экране банкомата для получения наличных:\
                    \n*{utils.numbers_format(amount_currency)} {currency}* ⏩ *{utils.numbers_format(amount_thb)} THB*\
                    '''

    elif language == 'eng':
        reply_text = f'''
                     \nPress *"confirm"* on the ATM screen to get cash:\
                     \n*{utils.numbers_format(amount_currency)} {currency}* ⏩ *{utils.numbers_format(amount_thb)} THB*\
                     '''
    
    return reply_text


def final_status(language, exchange_id, exchange_status, user_id, amount_currency, currency, amount_thb, status, rate_time):
    if language == 'rus':
        if exchange_status == 'success':
            exchange_status = 'успешный'
        else:
            exchange_status = 'неуспешный'

        reply_text = f'''
                    \nОбмен (*ID: {1000 + exchange_id}*) помечен как {exchange_status}:\
                    \n*{utils.numbers_format(amount_currency)} {currency}* ⏩ *{utils.numbers_format(amount_thb)} THB*\
                    \n\
                    \nЕсли у вас остались вопросы - свяжитесь с менеджером.\
                    '''

    elif language == 'eng':
        if exchange_status == 'success':
            exchange_status = 'success'
        else:
            exchange_status = 'failed'

        reply_text = f'''
                     \nExchange (*ID: {1000 + exchange_id}*) marked as {exchange_status}:\
                     \n*{utils.numbers_format(amount_currency)} {currency}* ⏩ *{utils.numbers_format(amount_thb)} THB*\
                     \n\
                     \nIf you have some questions - please contact manager.\
                     '''
    
    return reply_text