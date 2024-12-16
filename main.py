import telebot
import logging
import threading
import os
import inspect
import datetime

import config
import utils
import functions
import keyboards
import text
import db_functions

logging.basicConfig(level=logging.ERROR, 
                    filename="py_log.log", 
                    filemode="w", 
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    )

threading.Thread(daemon=True, target=functions.set_basic_exchange_rate).start()
threading.Thread(daemon=True, target=functions.set_specific_exchange_rate).start()
threading.Thread(daemon=True, target=functions.daily_notify).start()

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    """Handles the 'start' command.
    Sends a welcome message, adds new users to database,
    parse their referrals, adds keyboards.
    """
    
    # adds a new user and his referral
    threading.Thread(daemon=True, 
                            target=functions.handle_start_command, 
                            args=(message,),
                            ).start()
    
    bot.send_message(chat_id=message.chat.id,
                     text=config.CHOOSE_LANGUAGE,
                     reply_markup=keyboards.languages_first_keyboard(),
                     )


@bot.message_handler(commands=['referral'])
def referral_message(message):
    """Handles 'referral' command. Displays one of two possible keyboards.
    (Get info about referral that already exists or register new referral).
    """

    language = functions.get_language(message.from_user.id)
    referral = utils.extract_referral(message.text, '/referral')

    # if entered referral is valid
    if referral != '':
        is_referral = functions.check_if_referral(referral)
        
        # if the referral exists
        if is_referral:
            if language == 'rus':
                reply_text = f'Реферал *{referral}* уже существует.'
            else:
                reply_text = f'Referral *{referral}* already exists.'

            bot.send_message(chat_id=message.chat.id,
                             text=reply_text,
                             parse_mode='Markdown',
                             reply_markup=keyboards.send_referral_keyboard(referral, language),
                             disable_notification=True,
                             )
        
        # register new referral
        else:
            if language == 'rus':
                reply_text = f'Зарезервировать *{referral}*?'
            else:
                reply_text = f'Reserve *{referral}*?'

            bot.send_message(chat_id=message.chat.id,
                             text=reply_text,
                             parse_mode='Markdown',
                             reply_markup=keyboards.reserve_referral_keyboard(referral, language),
                             disable_notification=True,
                             )

    # referral format not valid
    else:
        bot.send_message(chat_id=message.chat.id,
                        text=config.INCORRECT_REFERRAL_MESSAGE[language],
                        parse_mode='Markdown',
                        disable_notification=True,
                        )


@bot.message_handler(commands=['exchange'])
def exchange_message(message):
    """Adds amount to referral."""
    
    language = 'rus'

    # check permissions
    if str(message.from_user.id) in config.MANAGER_ID or str(message.from_user.id) in config.DIRECTOR_ID: 
        command_data = utils.extract_amount_username(message.text)
        
        # checks command format
        if command_data:
            username = command_data[0]
            amount = command_data[1]

            referral = functions.get_users_referral(username)
            text_amount = utils.numbers_format(amount)

            # check if there is such referral
            if referral:
                bot.send_message(chat_id=message.chat.id,
                                 text=f'Учесть для реферала *{referral}* обмен на сумму *{text_amount}* бат?',
                                 reply_markup=keyboards.confirm_exchange_keyboard(referral, amount, language),
                                 parse_mode='Markdown',
                                 disable_notification=True,
                                 )
            
            # no such referral
            else:
                bot.send_message(chat_id=message.chat.id,
                                text=config.NO_REFERRAL_MESSAGE[language],
                                parse_mode='Markdown',
                                disable_notification=True,
                                )
        
        # wrong command format
        else:
            bot.send_message(chat_id=message.chat.id,
                                text=config.WRONG_FORMAT_MESSAGE[language],
                                disable_notification=True,
                                )
    
    # no permissions
    else:
        bot.send_message(chat_id=message.chat.id,
                                text=config.NO_PERMISSION_MESSAGE,
                                disable_notification=True,
                                )


@bot.message_handler(commands=['all'])
def all_referrals_message(message):
    """Provides information about all referrals."""

    language = 'rus'

    # check permissions
    if str(message.from_user.id) in config.DIRECTOR_ID:

        referrals = functions.get_all_referrals()
        replies = functions.construct_all_referrals_message(referrals)

        for reply in replies:
            try:
                bot.send_message(chat_id=message.chat.id,
                                 text=reply,
                                 parse_mode='Markdown',
                                 disable_notification=True,
                                 )
            except:
                logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось отправить сообщение по команде all.')

    # no permissions
    else:
        bot.send_message(chat_id=message.chat.id,
                                text=config.NO_PERMISSION_MESSAGE[language],
                                disable_notification=True,
                                )


@bot.message_handler(commands=['bonus'])
def all_referrals_message(message):
    """Provides information about all referrals."""

    language = 'rus'

    # check permissions
    if str(message.from_user.id) in config.DIRECTOR_ID:
        bonus_info = message.text.split(' ')

        if len(bonus_info) == 3:
            referral = bonus_info[1]
            referral_info = functions.get_referral(referral)

            if referral_info != []:
                bonus = utils.validate_bonus(bonus_info[2])

                if bonus:
                    db_functions.update_referral_field_info(referral_info.referral, 'percent', bonus)

                    bot.send_message(chat_id=message.chat.id,
                            text=f'Бонус *{referral_info.referral}* ({referral_info.identifier}) изменен на *{int(bonus * 100)}%*.',
                            parse_mode='Markdown',
                            disable_notification=True,
                            )
                
                else:
                    bot.send_message(chat_id=message.chat.id,
                            text='Введен неверный процент.',
                            disable_notification=True,
                            )

            else:
                bot.send_message(chat_id=message.chat.id,
                                text=config.WRONG_REFERRAL_MESSAGE[language],
                                disable_notification=True,
                                )
        
        else:
            bot.send_message(chat_id=message.chat.id,
                            text='Неверный формат, укажите команду, затем реферала, затем новый бонус.',
                            disable_notification=True,
                            )

    # no permissions
    else:
        bot.send_message(chat_id=message.chat.id,
                                text=config.NO_PERMISSION_MESSAGE[language],
                                disable_notification=True,
                                )


@bot.message_handler(commands=['balance'])
def get_referrals_balance(message):
    """Gets referral's balance."""

    language = functions.get_language(message.from_user.id)

    referral = utils.extract_referral(message.text, '/balance')
    referral_info = functions.get_referral(referral)

    # there is such referral
    if referral_info != []:
        amount = utils.numbers_format(referral_info.amount)
        if language == 'rus':
            bot.send_message(chat_id=message.chat.id,
                            text=f'На счету *{referral}* ({referral_info.identifier}) *{amount}* бат, бонус {int(referral_info.percent * 100)}% - свяжитесь с администратором, чтобы изменить.',
                            parse_mode='Markdown',
                            disable_notification=True,
                            )
        else:
            bot.send_message(chat_id=message.chat.id,
                            text=f'Account *{referral}* ({referral_info.identifier}) *{amount}* thb, bonus {int(referral_info.percent * 100)}% - contact administrator to change.',
                            parse_mode='Markdown',
                            disable_notification=True,
                            )
    
    # no such referral
    else:
        bot.send_message(chat_id=message.chat.id,
                        text=config.WRONG_REFERRAL_MESSAGE[language],
                        disable_notification=True,
                        )


@bot.message_handler(commands=['paid_all'])
def reduce_referrals_message(message):
    """Sets all referrals amount to 0."""

    language = 'rus'
    # check permissions
    if str(message.from_user.id) in config.DIRECTOR_ID:
        bot.send_message(chat_id=message.chat.id,
                         text=config.REDUCE_BALANCE_MESSAGE[language],
                         reply_markup=keyboards.confirm_reduce_all_keyboard(language),
                         disable_notification=True,
                         )
    
    # no permissions
    else:
        bot.send_message(chat_id=message.chat.id,
                        text=config.NO_PERMISSION_MESSAGE[language],
                        disable_notification=True,
                        )


@bot.message_handler(commands=['paid'])
def reduce_referrals_message(message):
    """Sets all referrals amount to 0."""

    language = 'rus'

    # check permissions
    if str(message.from_user.id) in config.DIRECTOR_ID:
        referral = utils.extract_referral(message.text, '/paid')
        is_referral = functions.check_if_referral(referral)

        # if there is such referral
        if is_referral:
            # get referral information
            referral_info = functions.get_referral(referral)

            amount = utils.numbers_format(referral_info.amount)
            reply_text = f'Обнулить счет *{referral}* ({referral_info.identifier})? (текущий баланс счета *{amount}* бат)'

            # ask confirmation to reduce the balance
            bot.send_message(chat_id=message.chat.id,
                            text=reply_text,
                            reply_markup=keyboards.confirm_reduce_keyboard(referral, language),
                            parse_mode='Markdown',
                            disable_notification=True,
                            )
        
        # no such referral
        else:
            bot.send_message(chat_id=message.chat.id,
                        text=config.WRONG_REFERRAL_MESSAGE[language],
                        disable_notification=True,
                        )
    
    # no permissions
    else:
        bot.send_message(chat_id=message.chat.id,
                        text=config.NO_PERMISSION_MESSAGE[language],
                        disable_notification=True,
                        )
        

@bot.message_handler(commands=['menu'])
def menu_message(message):
    """Displays menu without a large text."""

    language = functions.get_language(message.from_user.id)

    bot.send_message(message.chat.id, 
                    text=config.MAIN_MENU_MESSAGE[language], 
                    parse_mode='Markdown',
                    reply_markup=keyboards.main_keyboard(language),
                    disable_notification=True,
                    )
    

@bot.message_handler(commands=['rate'])
def rate_message(message):
    """Displays rate with menu button."""

    language = functions.get_language(message.from_user.id)

    bot.send_message(message.chat.id, 
                    text=functions.currency_rate_message(language), 
                    parse_mode='Markdown',
                    reply_markup=keyboards.menu_keyboard(language),
                    disable_notification=True,
                    )


@bot.message_handler(commands=['cancel_transfer'])
def rate_message(message):
    user_id = str(message.from_user.id)
    language = functions.get_language(message.from_user.id)

    input_data = db_functions.get_user_field_info(user_id, 'input_data')
    if input_data and 'slip' in input_data:
        exchange_id = int(input_data.split('_')[-1])
        db_functions.delete_exchange(exchange_id)

        bot.send_message(chat_id=message.chat.id,
                         text=text.TRANSFER_DECLINED[language],
                         parse_mode='Markdown',
                         disable_notification=True,
                         )
    
    else:
        bot.send_message(chat_id=message.chat.id,
                         text=text.NO_CURRENT_TRANSFER[language],
                         parse_mode='Markdown',
                         disable_notification=True,
                         )


@bot.callback_query_handler(func = lambda call: True)
def callback_query(call):
    """Handles queries from inline keyboards."""

    # getting message's and user's ids
    message_id = call.message.id
    chat_id=call.message.chat.id
    user_id = call.from_user.id

    call_data = call.data.split('_')
    query = call_data[0]
    language = call_data[1]

    if query == 'language':

        if language == 'change':
            bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=config.CHOOSE_LANGUAGE,
                                )
            bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=keyboards.languages_keyboard(),
                                            )
        
        else:
            first = call_data[2]

            functions.set_language(user_id, language)

            try:
                bot.delete_message(chat_id, message_id)
            except:
                pass

            try:
                if first == 'first':
                    bot.send_message(chat_id, 
                                        text=functions.currency_rate_message(language), 
                                        parse_mode='Markdown',
                                        disable_notification=True,
                                        )
                bot.send_message(chat_id, 
                            text=config.MAIN_MENU_MESSAGE[language], 
                            parse_mode='Markdown',
                            reply_markup=keyboards.main_keyboard(language),
                            disable_notification=True,
                            )
            except:
                pass

    # if the query have relations with referral actions
    elif query == 'referral':
        action = call_data[2]
        referral = call_data[3]

        # if user want's to get referral link and qr-code
        if action == 'info':
            # generate referral link based on referral
            coeff = db_functions.get_referral_field_info(referral, 'percent')
            if language == 'rus':
                bot.edit_message_text(message_id=message_id,
                                    chat_id=chat_id,
                                    text=f'Реферальная ссылка для {referral}: {config.BOT_LINK}?start={referral}.\n\nВаш бонус *{int(coeff * 100)}%* - для изменения обратитесь к администратору.',
                                    )
            else:
                bot.edit_message_text(message_id=message_id,
                                    chat_id=chat_id,
                                    text=f'Referral link for {referral}: {config.BOT_LINK}?start={referral}\n\nYour bonus *{int(coeff * 100)}%* - contact administrator to change.',
                                    )
            
            # generate qr-code based on referral link
            functions.generate_qr(referral, user_id)

            try:
                # open the generated qr-code png image
                with open(f'{user_id}.png', "rb") as file:
                    qr_bytes = file.read()

                # send the qr to user
                bot.send_photo(chat_id, photo=qr_bytes)

                # deletes the image from server
                os.remove(f'{user_id}.png')

            # log if there are errors
            except Exception as ex:
                logging.error(f'{inspect.currentframe().f_code.co_name}: При генерации и отправки qr-кода пользователю {user_id} произошла ошибка: {ex}.')

        # if user wants to reserve a referral
        elif action == 'reserve':
            bot.delete_message(chat_id, message_id)

            if language == 'rus':
                reply_text = f'Для резервирования реферала *{referral}* - в ответ на это сообщение укажите имя или название компании.'
                placeholder = 'Имя/название компании'
            else:
                reply_text = f'To reserve a referral *{referral}* - in response to this message, enter your name or company name.'
                placeholder = 'Name/company name'

            # ask for identifier as reply to the message
            bot.send_message(chat_id=chat_id,
                            text=reply_text,
                            reply_markup=telebot.types.ForceReply(input_field_placeholder=placeholder),
                            parse_mode='Markdown',
                            disable_notification=True,
                            )
        
        # if manager wants to register an exchange
        elif action == 'increase':
            # get exchange amount
            amount = float(call_data[4])

            # get referral object that contains all info needed
            referral_info = functions.get_referral(referral)

            # calculates the amount that should be on referral's account
            new_amount = round(referral_info.amount + amount * config.PROFIT_COEFF * referral_info.percent, 2)

            # change the referral balance amount
            functions.change_referral_amount(referral, new_amount)
            new_amount = utils.numbers_format(new_amount)

            if language == 'rus':
                reply_text = f'Обмен пользователя учтен, на счету *{referral}* ({referral_info.identifier}) *{new_amount}* бат.'
            else:
                reply_text = f"User's exchange accounted for *{referral}* ({referral_info.identifier}) *{new_amount}* baht."

            bot.edit_message_text(message_id=message_id,
                                chat_id=chat_id,
                                text=reply_text,
                                parse_mode='Markdown',
                                )
            
        # if director wants to reduce referral balance to 0
        elif action == 'reduce':
            
            # reduces all referrals balances
            if referral == 'all':
                threading.Thread(daemon=True, 
                            target=functions.reduce_all_referrals_balance, 
                            ).start()
                
                bot.edit_message_text(message_id=message_id,
                                chat_id=chat_id,
                                text=config.REDUCED_BALANCE_MESSAGE[language],
                                )
                
            # reduce the referral balance to 0
            else:
                threading.Thread(daemon=True, 
                            target=functions.reduce_referral_balance, 
                            args=(referral,),
                            ).start()
                
                if language == 'rus':
                    reply_text = f'Баланс *{referral}* обнулен.'
                else:
                    reply_text = f'*Balance of {referral} reduced.*'

                bot.edit_message_text(message_id=message_id,
                                chat_id=chat_id,
                                text=reply_text,
                                parse_mode='Markdown',
                                )
    
    # cancel the action, deletes keyboard and changes message
    elif query == 'cancel':
        bot.edit_message_text(message_id=message_id,
                                chat_id=chat_id,
                                text=config.CANCEL_MESSAGE[language],
                                )     
        
    elif query == 'menu':
        bot.edit_message_reply_markup(chat_id=chat_id,
                                      message_id=message_id,
                                      reply_markup=telebot.types.InlineKeyboardMarkup(),
                                      )
        
        bot.send_message(chat_id=chat_id, 
                    text=config.MAIN_MENU_MESSAGE[language], 
                    parse_mode='Markdown',
                    reply_markup=keyboards.main_keyboard(language),
                    disable_notification=True,
                    )
        
    elif query == 'exchanged':
        currency = call_data[2]
        exchange_type = call_data[3]

        bot.edit_message_reply_markup(chat_id=chat_id,
                                      message_id=message_id,
                                      reply_markup=keyboards.manager_application_keyboard(currency, exchange_type, language),
                                      )
        
        bot.send_message(chat_id=chat_id, 
                    text=config.MAIN_MENU_MESSAGE[language], 
                    parse_mode='Markdown',
                    reply_markup=keyboards.main_keyboard(language),
                    disable_notification=True,
                    )
        
    elif query == 'sended':
        bot.edit_message_reply_markup(chat_id=chat_id,
                                      message_id=message_id,
                                      reply_markup=keyboards.only_manager_keyboard(language),
                                      )
        
        bot.send_message(chat_id=chat_id, 
                    text=config.MAIN_MENU_MESSAGE[language], 
                    parse_mode='Markdown',
                    reply_markup=keyboards.main_keyboard(language),
                    disable_notification=True,
                    )
    
    elif query == 'recalculate':
        currency = call_data[2]
        exchange_type = call_data[3]

        if language == 'rus':
            reply_text = f'''
                        \nНажмите кнопку *"{currency}"*, если хотите обменять определенную сумму в *{currency} на THB*.\
                        \n\
                        \nНажмите кнопку *"THB"*, если хотите получить определенную сумму в *THB* в обмен на *{currency}*.\
                        '''
        else:
            reply_text = f'''
                         \nPress the *"{currency}"* button if you want to exchange a certain amount of *{currency} to THB*.\
                         \n\
                         \nPress the *"THB"* button if you want to receive a certain amount of *THB* in exchange for *{currency}*.\
                         '''
        
        bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=reply_text,
                                parse_mode='Markdown',
                                )
        bot.edit_message_reply_markup(chat_id=chat_id,
                                        message_id=message_id,
                                        reply_markup=keyboards.amount_currency_keyboard(currency, exchange_type, language),
                                        )
        
    elif query == 'service':
        bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.SERVICE_MESSAGE[language],
                                  parse_mode='Markdown',
                                  )
        bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.service_keyboard(language),
                                          )
    
    elif query == 'faq':
        bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.QUESTION_MESSAGE[language],
                                  parse_mode='Markdown',
                                  )
        bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.question_keyboard(language),
                                          )
    
    elif query == 'atm':
        bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.ATM_MESSAGE[language],
                                  parse_mode='Markdown'
                                  )
        bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.atm_keyboard(query, language),
                                          )

    elif query == 'airport':
        bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.AIRPORT_MESSAGE[language],
                                  parse_mode='Markdown',
                                  )
        bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.back_faq_keyboard(query, language),
                                          )
        
    elif query == 'delivery':
        bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.DELIVERY_MESSAGE[language],
                                  parse_mode='Markdown',
                                  )
        bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.back_faq_keyboard(query, language),
                                          )
        
    elif query == 'transfer':
        bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.TRANSFER_MESSAGE[language],
                                  parse_mode='Markdown',
                                  )
        bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.back_faq_keyboard(query, language),
                                          )
        
    elif query == 'banks':
        bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.BANKS_MESSAGE[language],
                                  parse_mode='Markdown',
                                  )
        bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.only_back_keyboard(language),
                                          )
    
    elif query == 'bangkok':
        try:
            bot.delete_message(chat_id, message_id)
        except:
            pass
        
        try:
            bot.send_document(chat_id=chat_id,
                            document=config.BANGKOK_FILE,
                            reply_markup=keyboards.back_atm_keyboard(language),
                            )

        except:
            pass
    
    elif query == 'kasikorn':
        try:
            bot.delete_message(chat_id, message_id)
        except:
            pass
        
        try:
            bot.send_document(chat_id=chat_id,
                            document=config.KASIKORN_FILE,
                            reply_markup=keyboards.back_atm_keyboard(language),
                            )

        except:
            pass
    
    elif query == 'krungsri':
        try:
            bot.delete_message(chat_id, message_id)
        except:
            pass

        bot.send_document(chat_id=chat_id,
                          document=config.KRUNGSRI_FILE,
                          reply_markup=keyboards.back_atm_keyboard(language),
                          )

    elif query == 'calculate':
        source = call_data[2]
        bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.PAIRS_MESSAGE[language],
                                  parse_mode='Markdown',
                                  )
        bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.pairs_keyboard(source, language),
                                          )

    elif query == 'exchange':
        currency = call_data[2]

        if len(call_data) == 3:
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.EXCHANGE_TYPE_MESSAGE[language],
                                  parse_mode='Markdown',
                                  )
            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.exchange_type_keyboard(currency, language),
                                          )
        
        elif len(call_data) == 4:
            exchange_type = call_data[3]

            if exchange_type != 'choose':
                if language == 'rus':
                    if exchange_type != 'service':
                        reply_text = f'''
                                    \nКнопка *{currency}*: введите сумму в *{currency}*, которую хотите обменять и я напишу, сколько *THB* Вы получите.\
                                    \n\
                                    \nКнопка *THB*: введите сумму в *THB*, которую хотите получить и я напишу, сколько *{currency}* Вам нужно обменять.\
                                    '''
                    else:
                        reply_text = f'''
                                    \nКнопка *{currency}*: введите сумму, которую хотите оплатить в *{currency}*.\
                                    \n\
                                    \nКнопка *THB*: введите сумму, которую хотите оплатить в *THB*.\
                                    '''
                else:
                    if exchange_type != 'service':
                        reply_text = f'''
                                    \n*{currency}* button: enter the amount of *{currency}* you want to exchange and I will let you know how much *THB* you will receive.\
                                    \n\
                                    \n*THB* button: enter the *THB* amount you want to receive and I will let you know how much *{currency}* you need to exchange.\
                                    '''
                    else:
                        reply_text = f'''
                                    \nButton *{currency}*: enter the amount you want to pay in *{currency}*.\
                                    \n\
                                    \n*THB* button: Enter the amount you want to pay in *THB*.\
                                    '''
                                
                bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=reply_text,
                                    parse_mode='Markdown',
                                    )
                bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=keyboards.amount_currency_keyboard(currency, exchange_type, language),
                                            )
            else:
                if language == 'rus':
                    reply_text = 'Выберите подходящий район доставки:'
                else:
                    reply_text = 'Select the appropriate delivery area:'

                bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=reply_text,
                                    parse_mode='Markdown',
                                    )
                bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=keyboards.delivery_types_keyboard(currency, language),
                                            )

        elif len(call_data) == 5:
            exchange_type = call_data[3]
            amount_currency = call_data[4]

            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except:
                pass

            
            minimal_amount = utils.numbers_format(config.TYPE_AMOUNT[exchange_type]).replace(' ', '.')

            if language == 'rus':
                translated_exchange_type = config.TYPE_RUSSIAN[exchange_type]
                reply_text = f'''
                        \nСпособ обмена: *{translated_exchange_type}*\
                        \nПара: *{currency}/THB*\
                        \n\
                        \nВ ответ на это сообщение введите сумму в *{amount_currency}* (*не менее {minimal_amount} THB*) для расчета актуального курса.\
                        '''
                placeholder = f'Сумма в {amount_currency}'

            else:
                translated_exchange_type = config.TYPE_ENGLISH[exchange_type]
                reply_text = f'''
                        \nExchange method: *{translated_exchange_type}*\
                        \nPair: *{currency}/THB*\
                        \n\
                        \nIn response to this message, enter the amount in *{amount_currency}* (*at least {minimal_amount} THB*) to calculate the current exchange rate.\
                        '''
                placeholder = f'Amount in {amount_currency}'

            bot.send_message(chat_id=chat_id,
                             text=reply_text,
                             reply_markup=telebot.types.ForceReply(input_field_placeholder=placeholder),
                             parse_mode='Markdown',
                             disable_notification=True,
                             )
            
    elif query == 'send':
        referral = db_functions.get_user_field_info(user_id, 'referral')
        if referral:
            try:
                thb_amount = int(float(call_data[2]))
                reply_markup = keyboards.referral_approve_keyboard(referral, thb_amount)
            except:
                reply_markup = telebot.types.InlineKeyboardMarkup()
        else:
            reply_markup = telebot.types.InlineKeyboardMarkup()

        user_message = call.message.text.replace(config.ADDITIONAL_MESSAGE[language], '')

        if language == 'rus':
            reply_text = 'Ваша заявка отправлена ✅\n\n' + user_message + 'Менеджер свяжется с вами в ближайшее время, также вы можете самостоятельно написать нашему менеджеру 👇'
        else:
            reply_text = 'Your application has been sent ✅\n\n' + user_message + 'The manager will contact you shortly, you can also contact to our manager yourself 👇'

        bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=reply_text,
                                  )
        bot.edit_message_reply_markup(chat_id=chat_id,
                                        message_id=message_id,
                                        reply_markup=keyboards.manager_keyboard(language),
                                        )
        
        try:
            reply_text = f'Пользователь @{call.from_user.username} получил следующий расчет:\n\n' + user_message
            
            if referral:
                reply_text += '\nПометьте, успешно ли прошла сделка, что начислить бонусы рефералу, от которого перешел пользователь.'

            for admin_id in config.MANAGER_ID:
                try:
                    bot.send_message(chat_id=admin_id,
                                reply_markup=reply_markup,
                                text=reply_text,
                                disable_notification=True,
                                )
                except:
                    pass
        except:
            pass

    elif query == 'back':
        destination = call_data[2]

        if destination == 'main':
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.MAIN_MENU_MESSAGE[language],
                                  )
            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.main_keyboard(language),
                                          )
        
        elif destination == 'faq':
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.QUESTION_MESSAGE[language],
                                  parse_mode='Markdown',
                                  )
            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.question_keyboard(language),
                                          )
            
        elif destination == 'leave':
            try:
                bot.edit_message_reply_markup(chat_id=chat_id,
                                                message_id=message_id,
                                                reply_markup=telebot.types.InlineKeyboardMarkup(),
                                                )
            except:
                pass

            final_destination = call_data[3]

            if final_destination == 'main':
                bot.send_message(chat_id=chat_id, 
                    text=config.MAIN_MENU_MESSAGE[language], 
                    parse_mode='Markdown',
                    reply_markup=keyboards.main_keyboard(language),
                    disable_notification=True,
                    )
                
            elif final_destination == 'atm':
                bot.send_message(chat_id=chat_id,
                                  text=config.ATM_MESSAGE[language],
                                  reply_markup=keyboards.atm_keyboard(final_destination, language),
                                  parse_mode='Markdown',
                                  disable_notification=True,
                                  )

        elif destination == 'pairs':
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.PAIRS_MESSAGE[language],
                                  parse_mode='Markdown',
                                  )
            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.pairs_keyboard('main', language),
                                          )
            
        elif destination == 'type':
            currency = call_data[3]

            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.EXCHANGE_TYPE_MESSAGE[language],
                                  parse_mode='Markdown',
                                  )
            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.exchange_type_keyboard(currency, language),
                                          )
            
        elif destination == 'airport':
            bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=config.AIRPORT_MESSAGE[language],
                                    parse_mode='Markdown',
                                    )
            bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=keyboards.back_faq_keyboard(destination, language),
                                            )
            
        elif destination == 'delivery':
            bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=config.DELIVERY_MESSAGE[language],
                                    parse_mode='Markdown',
                                    )
            bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=keyboards.back_faq_keyboard(destination, language),
                                            )
            
        elif destination == 'transfer':
            bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=config.TRANSFER_MESSAGE[language],
                                    parse_mode='Markdown',
                                    )
            bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=keyboards.back_faq_keyboard(destination, language),
                                            )
            
        elif destination == 'banks':
            bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=config.BANKS_MESSAGE[language],
                                    parse_mode='Markdown',
                                    )
            bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=keyboards.back_faq_keyboard(destination, language),
                                            )
        
        elif destination == 'atm':
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.ATM_MESSAGE[language],
                                  parse_mode='Markdown'
                                  )
            bot.edit_message_reply_markup(chat_id=chat_id,
                                message_id=message_id,
                                reply_markup=keyboards.atm_keyboard(query, language),
                                )
        
    elif query == 'reviews':
        try:
            bot.delete_message(chat_id, message_id)
        except:
            pass

        bot.send_media_group(chat_id=chat_id,
                          media=config.REVIEWS_MEDIA_IMAGES,
                          )
        
        if language =='rus':
            reply_text='Нажмите для возврата в меню:'
        else:
            reply_text='Press to return to menu:'

        bot.send_message(chat_id=chat_id,
                         text=reply_text, 
                         reply_markup=keyboards.menu_keyboard(language),
                         )

    elif query == 'cash':
        exchange_id = int(call_data[2])

        if db_functions.get_exchange_field_info(exchange_id, 'status') == 'creating':
            amount_thb = db_functions.get_exchange_field_info(exchange_id, 'amount_thb')

            time_curr = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).time()
            if datetime.time(hour=10, minute=0) <= time_curr and datetime.time(hour=20, minute=0) >= time_curr:
                if amount_thb % 100 == 0 and amount_thb <= config.MAX_AMOUNT:
                    try:
                        bot.edit_message_reply_markup(chat_id=chat_id,
                                                    message_id=message_id,
                                                    reply_markup=telebot.types.InlineKeyboardMarkup(),
                                                    )
                    except:
                        pass

                    rate_time = db_functions.get_exchange_field_info(exchange_id, 'rate_time')
                    current_time = datetime.datetime.utcnow() + datetime.timedelta(hours=7)

                    if current_time - datetime.timedelta(minutes=10) < rate_time:
                        exchange_info = db_functions.select_exchange_info(exchange_id)

                        if exchange_info[2] == 'USDT':
                            bot.send_message(chat_id=chat_id,
                                            text=config.CRYPTO_WALLET,
                                            parse_mode='Markdown',
                                            disable_notification=True,
                                            )

                        elif exchange_info[2] == 'RUB':
                            bot.send_message(chat_id=chat_id,
                                            text=config.ACCOUNT,
                                            parse_mode='Markdown',
                                            disable_notification=True,
                                            )
                            
                            bot.send_message(chat_id=chat_id,
                                            text=config.NUMBER,
                                            parse_mode='Markdown',
                                            disable_notification=True,
                                            )

                        bot.send_message(chat_id=chat_id,
                                        text=text.confirm_payment(language, exchange_id, *exchange_info),
                                        reply_markup=keyboards.transferred_keyboard(language, exchange_id),
                                        parse_mode='Markdown',
                                        )

                    else:
                        db_functions.delete_exchange(exchange_id)

                        bot.edit_message_text(chat_id=chat_id,
                                            message_id=message_id,
                                            text=text.OUTDATED_RATE[language],
                                            parse_mode='Markdown',
                                            )
                        
                        bot.edit_message_reply_markup(chat_id=chat_id,
                                                    message_id=message_id,
                                                    reply_markup=keyboards.menu_keyboard(language),
                                                    )
                
                else:
                    bot.answer_callback_query(callback_query_id=call.id,
                                            text=text.AMOUNT_RULES[language],
                                            show_alert=True,
                                            )
            
            else:
                bot.answer_callback_query(callback_query_id=call.id,
                                            text=text.TIME_RULES[language],
                                            show_alert=True,
                                            )

        else:
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=text.OUTDATED[language],
                                  parse_mode='Markdown',
                                  )
            
            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.menu_keyboard(language),
                                          )

    elif query == 'decline':
        exchange_id = int(call_data[2])
        subject = call_data[3]

        if subject == 'transfer':
            if db_functions.get_exchange_field_info(exchange_id, 'status') == 'creating':
                db_functions.delete_exchange(exchange_id)

                bot.edit_message_text(chat_id=chat_id,
                                      message_id=message_id,
                                      text=text.TRANSFER_DECLINED[language],
                                      parse_mode='Markdown',
                                      )
                    
            else:
                bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=text.OUTDATED[language],
                                    parse_mode='Markdown',
                                    )
                
                bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=keyboards.menu_keyboard(language),
                                            )

    elif query == 'transferred':
        exchange_id = int(call_data[2])

        if db_functions.get_exchange_field_info(exchange_id, 'status') == 'creating':
            rate_time = db_functions.get_exchange_field_info(exchange_id, 'rate_time')
            current_time = datetime.datetime.utcnow() + datetime.timedelta(hours=7)

            if current_time - datetime.timedelta(minutes=25) > rate_time:
                db_functions.update_exchange_field_info(exchange_id, 'outdated', True)

            db_functions.update_exchange_field_info(exchange_id, 'status', 'waiting_payment')
            db_functions.update_user_field_info(user_id, 'input_data', f'slip_{exchange_id}')

            bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=text.SEND_SLIP[language],
                                    parse_mode='Markdown',
                                    )
                
        else:
            bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=text.OUTDATED[language],
                                parse_mode='Markdown',
                                )
            
            bot.edit_message_reply_markup(chat_id=chat_id,
                                        message_id=message_id,
                                        reply_markup=keyboards.menu_keyboard(language),
                                        )
    
    elif query == 'receive':
        action = call_data[1]
        exchange_id = int(call_data[2])

        try:
            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=telebot.types.InlineKeyboardMarkup(),
                                          )
        except:
            pass

        if db_functions.get_exchange_field_info(exchange_id, 'status') == 'waiting_confirm_payment':
            client_id = db_functions.get_exchange_field_info(exchange_id, 'user_id')
            client_language = db_functions.get_user_field_info(client_id, 'language')

            if action == 'confirm':
                db_functions.update_exchange_field_info(exchange_id, 'status', 'waiting_atm')
                bot.send_message(chat_id=chat_id,
                             text=text.ADMIN_RECEIVED,
                             parse_mode='Markdown',
                             reply_to_message_id=message_id,
                             )
                
                try:
                    bot.send_message(chat_id=client_id,
                                     text=text.TRANSFER_CONFIRMED_BY_ADMIN[client_language],
                                     reply_markup=keyboards.confirm_atm_keyboard(client_language, exchange_id),
                                     parse_mode='Markdown',
                                     )
                except:
                    pass

            elif action == 'decline':
                db_functions.update_exchange_field_info(exchange_id, 'status', 'canceled')
                bot.send_message(chat_id=chat_id,
                             text=text.ADMIN_NO_RECEIVE,
                             parse_mode='Markdown',
                             reply_to_message_id=message_id,
                             )
                
                try:
                    bot.send_message(chat_id=client_id,
                                     text=text.TRANSFER_DECLINED_BY_ADMIN[client_language],
                                     reply_markup=keyboards.manager_keyboard(client_language),
                                     parse_mode='Markdown',
                                     )
                except:
                    pass

        else:
            bot.send_message(chat_id=chat_id,
                             text=text.ADMIN_OUTDATED,
                             parse_mode='Markdown',
                             reply_to_message_id=message_id,
                             )
    
    elif query == 'near-atm':
        exchange_id = int(call_data[2])

        if db_functions.get_exchange_field_info(exchange_id, 'status') == 'waiting_atm':
            db_functions.update_exchange_field_info(exchange_id, 'status', 'waiting_atm_confirm')

            exchange_info = db_functions.select_exchange_info(exchange_id)
            username = db_functions.get_user_field_info(user_id, 'user_username')
            
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=text.NEAR_ATM[language],
                                  parse_mode='Markdown',
                                  )
            
            for admin_id in config.MANAGER_ID:
                try:
                    bot.send_message(chat_id=admin_id,
                                    text=text.confirm_ready(exchange_id, username, *exchange_info),
                                    reply_markup=keyboards.ready_keyboard(exchange_id),
                                    parse_mode='Markdown',
                                    )
                except:
                    pass

        else:
            bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=text.OUTDATED[language],
                                parse_mode='Markdown',
                                )
            
            bot.edit_message_reply_markup(chat_id=chat_id,
                                        message_id=message_id,
                                        reply_markup=keyboards.menu_keyboard(language),
                                        )
    
    elif query == 'ready':
        exchange_id = int(call_data[1])

        if db_functions.get_exchange_field_info(exchange_id, 'status') == 'waiting_atm_confirm':
            db_functions.update_exchange_field_info(exchange_id, 'status', 'waiting_qr')

            client_id = db_functions.get_exchange_field_info(exchange_id, 'user_id')
            client_language = db_functions.get_user_field_info(client_id, 'language')

            exchange_info = db_functions.select_exchange_info(exchange_id)

            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=telebot.types.InlineKeyboardMarkup(),
                                          )
            
            bot.send_message(chat_id=chat_id,
                             text=text.ADMIN_WAITING_QR,
                             parse_mode='Markdown',
                             disable_notification=True,
                             )

            db_functions.update_user_field_info(client_id, 'input_data', f'qr_{exchange_id}')

            try:
                bot.send_message(chat_id=client_id,
                                 text=text.send_qr(client_language, exchange_id, *exchange_info),
                                 parse_mode='Markdown',
                                 )
            except:
                pass
        else:
            bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=text.ADMIN_OUTDATED,
                                parse_mode='Markdown',
                                )
    
    elif query == 'cash-atm':
        action = call_data[1]
        exchange_id = int(call_data[2])

        if db_functions.get_exchange_field_info(exchange_id, 'status') == 'waiting_finish':
            try:
                bot.edit_message_reply_markup(chat_id=chat_id,
                                              message_id=message_id,
                                              reply_markup=telebot.types.InlineKeyboardMarkup(),
                                              )
            except:
                pass

            client_id = db_functions.get_exchange_field_info(exchange_id, 'user_id')
            client_language = db_functions.get_user_field_info(client_id, 'language')
            exchange_info = db_functions.select_exchange_info(exchange_id)

            if action == 'done':
                db_functions.update_exchange_field_info(exchange_id, 'status', 'waiting_status')

                username = db_functions.get_user_field_info(client_id, 'user_username')

                bot.send_message(chat_id=chat_id,
                                 text=text.confirm_status(exchange_id, username, *exchange_info),
                                 reply_markup=keyboards.confirm_status_keyboard(exchange_id),
                                 parse_mode='Markdown',
                                 disable_notification=True,
                                 reply_to_message_id=message_id,
                                 )

                try:
                    bot.send_message(chat_id=client_id,
                                     text=text.press_confirm(client_language, *exchange_info),
                                     parse_mode='Markdown',
                                     )
                except Exception as ex:
                    print(ex)

            elif action == 'reenter':
                db_functions.update_user_field_info(client_id, 'input_data', f'qr_{exchange_id}')
                db_functions.update_exchange_field_info(exchange_id, 'status', 'waiting_qr')

                bot.send_message(chat_id=chat_id,
                                 text=text.ADMIN_ASKED_REENTER,
                                 parse_mode='Markdown',
                                 disable_notification=True,
                                 reply_to_message_id=message_id,
                                 )
                
                try:
                    bot.send_message(chat_id=client_id,
                                     text=text.resend_qr(client_language, *exchange_info),
                                     parse_mode='Markdown',
                                     )
                except:
                    pass

        else:
            bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=text.ADMIN_OUTDATED,
                                parse_mode='Markdown',
                                )

    elif query == 'status':
        status = call_data[1]
        exchange_id = int(call_data[2])

        if db_functions.get_exchange_field_info(exchange_id, 'status') == 'waiting_status':
            db_functions.update_exchange_field_info(exchange_id, 'status', status)

            try:
                bot.edit_message_reply_markup(message_id=message_id,
                                              chat_id=chat_id,
                                              reply_markup=telebot.types.InlineKeyboardMarkup(),
                                              )
            except:
                pass

            client_id = db_functions.get_exchange_field_info(exchange_id, 'user_id')
            client_language = db_functions.get_user_field_info(client_id, 'language')
            exchange_info = db_functions.select_exchange_info(exchange_id)
            
            if status == 'success':
                reply_admin_text = text.ADMIN_SUCCESS

                referral = db_functions.get_user_field_info(client_id, 'referral')
                if referral:
                    # get exchange amount
                    amount = exchange_info[3]

                    # get referral object that contains all info needed
                    referral_info = functions.get_referral(referral)

                    # calculates the amount that should be on referral's account
                    new_amount = round(referral_info.amount + amount * config.PROFIT_COEFF * referral_info.percent, 2)

                    # change the referral balance amount
                    functions.change_referral_amount(referral, new_amount)
                    new_amount = utils.numbers_format(new_amount)

                    reply_admin_text = f'Обмен пользователя учтен, на счету *{referral}* ({referral_info.identifier}) *{new_amount}* бат.'

            elif status == 'failed':
                reply_admin_text = text.ADMIN_FAILED

            reply_text = text.final_status(client_language, exchange_id, status, *exchange_info)

            bot.send_message(chat_id=chat_id,
                                text=reply_admin_text,
                                parse_mode='Markdown',
                                disable_notification=True,
                                reply_to_message_id=message_id,
                                )
            
            try:
                bot.send_message(chat_id=client_id,
                                 text=reply_text,
                                 reply_markup=keyboards.manager_keyboard(client_language),
                                 parse_mode='Markdown',
                                 )
            except:
                pass
                
        else:
            bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=text.ADMIN_OUTDATED,
                                parse_mode='Markdown',
                                )

    elif query == 'approve':
        status = call_data[1]

        try:
            bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=telebot.types.InlineKeyboardMarkup(),
                                            )
        except:
            pass

        if status == 'success':
            referral = call_data[2]
            amount = int(float(call_data[3]))

            # get referral object that contains all info needed
            referral_info = functions.get_referral(referral)

            # calculates the amount that should be on referral's account
            new_amount = round(referral_info.amount + amount * config.PROFIT_COEFF * referral_info.percent, 2)

            # change the referral balance amount
            functions.change_referral_amount(referral, new_amount)
            new_amount = utils.numbers_format(new_amount)

            reply_admin_text = f'Обмен пользователя учтен, на счету *{referral}* ({referral_info.identifier}) *{new_amount}* бат.'

            for admin_id in config.MANAGER_ID:
                try: 
                    bot.send_message(chat_id=admin_id,
                                        text=reply_admin_text,
                                        parse_mode='Markdown',
                                        )
                except:
                    pass

    elif query == 'address':
        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass

        bot.send_photo(chat_id=chat_id,
                      photo=config.OFFICE_PHOTO,
                      caption='',
                      reply_markup=keyboards.address_keyboard(language),
                      parse_mode='Markdown',
                      disable_notification=True,
                      )
    
    elif query == 'delete':
        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass

        bot.send_message(chat_id, 
                        text=config.MAIN_MENU_MESSAGE[language], 
                        parse_mode='Markdown',
                        reply_markup=keyboards.main_keyboard(language),
                        disable_notification=True,
                        )

    elif query == 'location':
        bot.send_location(chat_id=chat_id,
                          latitude=7.772229,
                          longitude=98.318038,
                          reply_markup=keyboards.menu_keyboard(language),
                          )


@bot.message_handler(content_types=['text'])
def handle_text(message):
    """Handles message with type text. Gets identifier if user wants to add referral."""

    language = functions.get_language(message.from_user.id)

    # check if the text is reply to a message with text that asks to enter identifier 
    # the "reply to" message should be sended by bot
    if str(message.from_user.id) in config.MANAGER_ID and '#рассылка' in message.text:
        message_to_send = message.text.replace('#рассылка', '')

        threading.Thread(daemon=True, 
                         target=functions.send_marketing_message, 
                         args=(message_to_send, 'text'),
                         ).start()

    elif (message.reply_to_message is not None) and\
    (config.CHECK_IDENTIFIER[language] in message.reply_to_message.text) and\
    (str(message.reply_to_message.from_user.id) == config.BOT_ID):
        # delete "reply to" message to avoid reuse
        try:
            bot.delete_message(message.chat.id, message.reply_to_message.id)
        except:
            pass

        identifier = message.text
        unique_identifier = functions.check_unique_identifier(identifier)

        referral = utils.extract_referral_from_message(message.reply_to_message.text, language)

        # if the entered identifier is unique
        if unique_identifier:
            # add referral to database
            threading.Thread(daemon=True, 
                            target=functions.add_referral, 
                            args=(identifier, referral,),
                            ).start()
            
            if language == 'rus':
                reply_text = f'Реферал *{referral}* успешно зарезервирован.\n\nВаш бонус *{int(config.REFERRAL_COEFF * 100)}%* - для изменения обратитесь к администратору.'
            else:
                reply_text = f'Referral *{referral}* reserved successfully.\n\nYour bonus *{int(config.REFERRAL_COEFF * 100)}%* - contact administrator to change.'

            bot.send_message(chat_id=message.chat.id,
                             text=reply_text,
                             parse_mode='Markdown',
                             disable_notification=True,
                             )
            
            user_id = message.from_user.id

            # generate qr-code
            functions.generate_qr(referral, user_id)

            if language == 'rus':
                link_text = f'Реферальная ссылка для {referral}: {config.BOT_LINK}?start={referral}'
            else:
                link_text = f'Referral link for {referral}: {config.BOT_LINK}?start={referral}'

            # send referral link
            bot.send_message(chat_id=message.chat.id,
                            text=link_text,
                            disable_notification=True,
                            )

            # send qr-code 
            try:
                # open qr-code image
                with open(f'{user_id}.png', "rb") as file:
                    qr_bytes = file.read()

                # send it to user
                bot.send_photo(message.chat.id, photo=qr_bytes)

                # delete the image from server
                os.remove(f'{user_id}.png')

            except Exception as ex:
                logging.error(f'{inspect.currentframe().f_code.co_name}: При генерации и отправки qr-кода пользователю {user_id} произошла ошибка: {ex}.')
        
        # identifier already exists
        else:
            if language == 'rus':
                reply_text = f'Такой идентификатор уже существует. Для резервирования реферала *{referral}* - в ответ на это сообщение укажите имя или название компании.'
                placeholder = 'Имя/название компании'
            else:
                reply_text = f'This identifier already exists. To reserve a referral *{referral}* - in response to this message, enter your name or company name'
                placeholder = 'Company name/name'

            bot.send_message(chat_id=message.chat.id,
                            text=reply_text,
                            reply_markup=telebot.types.ForceReply(input_field_placeholder=placeholder),
                            parse_mode='Markdown',
                            disable_notification=True,
                            )
            
    elif (message.reply_to_message is not None) and\
    ('Способ обмена' in message.reply_to_message.text or 'Exchange method: ' in message.reply_to_message.text) and\
    ('Курс:' not in message.reply_to_message.text and 'Rate:' not in message.reply_to_message.text) and\
    (str(message.reply_to_message.from_user.id) == config.BOT_ID): 
        currency, exchange_type, amount_currency = utils.extract_exchange_info(message.reply_to_message.text, language)

        amount = utils.convert_to_float(message.text)

        if language == 'rus':
            translated_exchange_type = config.TYPE_RUSSIAN[exchange_type]
        else:
            translated_exchange_type = config.TYPE_ENGLISH[exchange_type]

        minimal_amount = config.TYPE_AMOUNT[exchange_type]
        
        # if user entered a number
        if amount:
            user_id = message.from_user.id
            thb_amount = amount
            if amount_currency != 'THB':
                if currency == 'RUB':
                    thb_amount = round(amount / config.BASIC_RUB, 2)
                elif currency == 'USDT':
                    thb_amount = round(amount * config.BASIC_USDT, 2)
                elif currency == 'USD':
                    thb_amount = round(amount * config.BASIC_USD, 2)
            
            # if the entered amount more than minimal
            if thb_amount >= minimal_amount:
                exchange_rate = None
                tmp_amount = amount
                counter = 0
                while exchange_rate is None and counter != 3:
                    exchange_rate = functions.get_exchange_rate(currency=currency,
                                                            delivery_type=exchange_type,
                                                            amount_currency=amount_currency,
                                                            amount=tmp_amount,
                                                            )
                    tmp_amount = tmp_amount / 10
                    counter += 1

                if amount_currency == 'THB':
                    thb_amount = amount
                    if currency == 'RUB':
                        currency_amount = round(thb_amount * exchange_rate, 2)
                    if currency == 'USDT' or currency == 'USD':
                        currency_amount = round(thb_amount / exchange_rate, 2)
                
                else:
                    currency_amount = amount
                    if currency == 'RUB':
                        thb_amount = round(currency_amount / exchange_rate, 2)
                    if currency == 'USDT' or currency == 'USD':
                        thb_amount = round(currency_amount * exchange_rate, 2)

                real_currency_amount = currency_amount
                real_thb_amount = thb_amount 

                currency_amount = utils.numbers_format(currency_amount)
                thb_amount = utils.numbers_format(thb_amount)

                # delete "reply to" message to avoid reuse (duplicated to avoid long waiting time for user between delete and answer)
                try:
                    bot.delete_message(message.chat.id, message.reply_to_message.id)
                except:
                    pass
                
                if language == 'rus':
                    reply_text = f'''
                            \nСпособ обмена: *{translated_exchange_type}*\
                            \nПара: *{currency}/THB*\
                            \nКурс: *{exchange_rate}*\
                            \n\
                            \n*{currency_amount} {currency} ⏩ {thb_amount} THB*\
                            \n\
                            \n{config.ADDITIONAL_MESSAGE[language]}\
                            '''
                else:
                    reply_text = f'''
                             \nExchange method: *{translated_exchange_type}*\
                             \nPair: *{currency}/THB*\
                             \nRate: *{exchange_rate}*\
                             \n\
                             \n*{currency_amount} {currency} ⏩ {thb_amount} THB*\
                             \n\
                             \n{config.ADDITIONAL_MESSAGE[language]}\
                             '''

                ATM_FLAG = False
                creating_exchange_id = '-'
                if translated_exchange_type == 'ATM' or translated_exchange_type == 'банкомат':
                    ATM_FLAG = True

                    creating_exchange_id = db_functions.get_creating_exchange_id(user_id)
                    if creating_exchange_id:
                        db_functions.delete_exchange(creating_exchange_id)
                    
                    current_time = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
                    db_functions.add_exchange(user_id, real_currency_amount, currency, real_thb_amount, current_time)
                    creating_exchange_id = db_functions.get_creating_exchange_id(user_id)

                bot.send_message(chat_id=message.chat.id,
                                text=reply_text,
                                reply_markup=keyboards.exchanged_keyboard(currency, exchange_type, language, ATM_FLAG, creating_exchange_id, real_thb_amount),
                                parse_mode='Markdown',
                                disable_notification=True,
                                )

            # entered amount less then minimal
            else:
                # delete "reply to" message to avoid reuse (duplicated to avoid long waiting time for user between delete and answer)
                try:
                    bot.delete_message(message.chat.id, message.reply_to_message.id)
                except:
                    pass

                minimal_amount = utils.numbers_format(minimal_amount).replace(' ', '.')
                thb_amount = utils.numbers_format(thb_amount)

                if language == 'rus':
                    reply_text = f'''
                            \nВведенная сумма эквивалента *{thb_amount} THB*, что меньше допустимого минимума в *{minimal_amount} THB* для выбранного способа обмена. Попробуйте еще раз.\
                            \n\
                            \nСпособ обмена: *{translated_exchange_type}*\
                            \nПара: *{currency}/THB*\
                            \n\
                            \nВ ответ на это сообщение введите сумму в *{amount_currency}* (*не менее {minimal_amount} THB*) для расчета актуального курса.\
                            '''
                    placeholder = f'Сумма в {amount_currency}'
                else:
                    reply_text = f'''
                            \nThe entered amount is equivalent to *{thb_amount} THB*, which is less than the allowed minimum of *{minimal_amount} THB* for the selected exchange method. Try again.\
                            \n\
                            \nExchange method: *{translated_exchange_type}*\
                            \nPair: *{currency}/THB*\
                            \n\
                            \nIn response to this message, enter the amount in *{amount_currency}* (*at least {minimal_amount} THB*) to calculate the current exchange rate.\
                            '''
                    placeholder = f'Amount in {amount_currency}'
                    
                
                bot.send_message(chat_id=message.chat.id,
                                text=reply_text,
                                reply_markup=telebot.types.ForceReply(input_field_placeholder=placeholder),
                                parse_mode='Markdown',
                                disable_notification=True,
                                )
                
        # user entered not a number  
        else:
            # delete "reply to" message to avoid reuse (duplicated to avoid long waiting time for user between delete and answer)
            try:
                bot.delete_message(message.chat.id, message.reply_to_message.id)
            except:
                pass
            
            minimal_amount = utils.numbers_format(minimal_amount).replace(' ', '.')

            if language == 'rus':
                reply_text = f'''
                        \nВведенный ответ не является числом. Попробуйте еще раз.\
                        \n\
                        \nСпособ обмена: *{translated_exchange_type}*\
                        \nПара: *{currency}/THB*\
                        \n\
                        \nВ ответ на это сообщение введите сумму в *{amount_currency}* (*не менее {minimal_amount} THB*) для расчета актуального курса.\
                        '''
                placeholder = f'Сумма в {amount_currency}'
            else:
                reply_text = f'''
                        \nThe answer you entered is not a number. Try again.\
                        \n\
                        \nExchange method: *{translated_exchange_type}*\
                        \nPair: *{currency}/THB*\
                        \n\
                        \nIn response to this message, enter the amount in *{amount_currency}* (*at least {minimal_amount} THB*) to calculate the current exchange rate.\
                        '''
                placeholder = f'Amount in {amount_currency}'
          
            bot.send_message(chat_id=message.chat.id,
                             text=reply_text,
                             reply_markup=telebot.types.ForceReply(input_field_placeholder=placeholder),
                             parse_mode='Markdown',
                             disable_notification=True,
                             )


@bot.message_handler(content_types=['photo'])
def handle_text(message):
    #print(message)
    user_id = str(message.from_user.id)
    language = functions.get_language(user_id)

    input_data = db_functions.get_user_field_info(user_id, 'input_data')

    if str(user_id) in config.MANAGER_ID and message.caption and '#рассылка' in message.caption:
        photo = message.photo[-1].file_id
        message_to_send = message.caption.replace('#рассылка', '')

        threading.Thread(daemon=True, 
                         target=functions.send_marketing_message, 
                         args=(message_to_send, 'photo', photo),
                         ).start()

    elif input_data and 'slip' in input_data:
        exchange_id = int(input_data.split('_')[-1])

        if db_functions.get_exchange_field_info(exchange_id, 'status') == 'waiting_payment':
            db_functions.update_user_field_info(user_id, 'input_data', None)
            db_functions.update_exchange_field_info(exchange_id, 'status', 'waiting_confirm_payment')

            exchange_info = db_functions.select_exchange_info(exchange_id)
            photo = message.photo[-1].file_id
            username = db_functions.get_user_field_info(user_id, 'user_username')

            bot.send_message(chat_id=message.chat.id,
                             text=text.CHECK_TRANSFER[language],
                             parse_mode='Markdown',
                             disable_notification=True,
                             )
            
            for admin_id in config.MANAGER_ID:
                try:
                    bot.send_photo(chat_id=admin_id,
                                photo=photo,
                                caption=text.confirm_receive(exchange_id, username, *exchange_info),
                                reply_markup=keyboards.confirm_receive_keyboard(exchange_id),
                                parse_mode='Markdown',
                                )
                except:
                    pass
                
        else:
            bot.send_message(chat_id=message.chat.id,
                                text=text.OUTDATED[language],
                                reply_markup=keyboards.menu_keyboard(language),
                                parse_mode='Markdown',
                                )
    
    elif input_data and 'qr' in input_data:
        exchange_id = int(input_data.split('_')[-1])

        if db_functions.get_exchange_field_info(exchange_id, 'status') == 'waiting_qr':
            db_functions.update_user_field_info(user_id, 'input_data', None)
            db_functions.update_exchange_field_info(exchange_id, 'status', 'waiting_finish')

            exchange_info = db_functions.select_exchange_info(exchange_id)
            photo = message.photo[-1].file_id
            username = db_functions.get_user_field_info(user_id, 'user_username')

            bot.send_message(chat_id=message.chat.id,
                             text=text.QR_SENDED[language],
                             parse_mode='Markdown',
                             disable_notification=True,
                             )

            for admin_id in config.MANAGER_ID:
                try:
                    bot.send_photo(chat_id=admin_id,
                                photo=photo,
                                caption=text.confirm_cash(exchange_id, username, *exchange_info),
                                reply_markup=keyboards.confirm_cash_keyboard(exchange_id),
                                parse_mode='Markdown',
                                )
                except:
                    pass
                
        else:
            bot.send_message(chat_id=message.chat.id,
                                text=text.OUTDATED[language],
                                reply_markup=keyboards.menu_keyboard(language),
                                parse_mode='Markdown',
                                )


@bot.message_handler(content_types=['video'])
def handle_text(message):
    """Handles message with type text."""

    user_id = str(message.from_user.id)

    if user_id in config.MANAGER_ID and message.caption and '#рассылка' in message.caption:
        message_to_send = message.caption.replace('#рассылка', '')
        video = message.video.file_id

        threading.Thread(daemon=True, 
                         target=functions.send_marketing_message, 
                         args=(message_to_send, 'video', video),
                         ).start()


# @bot.message_handler(content_types=['document'])
# def handle_text(message):
#     print(message)


if __name__ == '__main__':
    #bot.polling(timeout=80)
    while True:
        try:
            bot.polling()
        except:
            pass
