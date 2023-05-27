import telebot
import logging
import threading
import os
import inspect

import config
import utils
import functions
import keyboards

logging.basicConfig(level=logging.INFO, 
                    filename="py_log.log", 
                    filemode="w", 
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    )

threading.Thread(daemon=True, target=functions.set_basic_exchange_rate).start()
threading.Thread(daemon=True, target=functions.set_specific_exchange_rate).start()

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
    try:
        bot.send_message(message.chat.id, 
                         text=functions.currency_rate_message(), 
                         parse_mode='Markdown',
                         disable_notification=True,
                         )
        bot.send_message(message.chat.id, 
                    text=config.MAIN_MENU_MESSAGE, 
                    parse_mode='Markdown',
                    reply_markup=keyboards.main_keyboard(),
                    disable_notification=True,
                    )
    except:
        pass


@bot.message_handler(commands=['referral'])
def referral_message(message):
    """Handles 'referral' command. Displays one of two possible keyboards.
    (Get info about referral that already exists or register new referral).
    """

    referral = utils.extract_referral(message.text, '/referral')

    # if entered referral is valid
    if referral != '':
        is_referral = functions.check_if_referral(referral)
        
        # if the referral exists
        if is_referral:
            bot.send_message(chat_id=message.chat.id,
                             text=f'Реферал *{referral}* уже существует.',
                             parse_mode='Markdown',
                             reply_markup=keyboards.send_referral_keyboard(referral),
                             disable_notification=True,
                             )
        
        # register new referral
        else:
            bot.send_message(chat_id=message.chat.id,
                             text=f'Зарезервировать *{referral}*?',
                             parse_mode='Markdown',
                             reply_markup=keyboards.reserve_referral_keyboard(referral),
                             disable_notification=True,
                             )

    # referral format not valid
    else:
        bot.send_message(chat_id=message.chat.id,
                        text=config.INCORRECT_REFERRAL_MESSAGE,
                        parse_mode='Markdown',
                        disable_notification=True,
                        )


@bot.message_handler(commands=['exchange'])
def exchange_message(message):
    """Adds amount to referral."""
    
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
                                 reply_markup=keyboards.confirm_exchange_keyboard(referral, amount),
                                 parse_mode='Markdown',
                                 disable_notification=True,
                                 )
            
            # no such referral
            else:
                bot.send_message(chat_id=message.chat.id,
                                text=config.NO_REFERRAL_MESSAGE,
                                parse_mode='Markdown',
                                disable_notification=True,
                                )
        
        # wrong command format
        else:
            bot.send_message(chat_id=message.chat.id,
                                text=config.WRONG_FORMAT_MESSAGE,
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
                                text=config.NO_PERMISSION_MESSAGE,
                                disable_notification=True,
                                )


@bot.message_handler(commands=['balance'])
def get_referrals_balance(message):
    """Gets referral's balance."""

    referral = utils.extract_referral(message.text, '/balance')
    referral_info = functions.get_referral(referral)

    # there is such referral
    if referral_info != []:
        amount = utils.numbers_format(referral_info.amount)
        bot.send_message(chat_id=message.chat.id,
                        text=f'На счету *{referral}* ({referral_info.identifier}) *{amount}* бат.',
                        parse_mode='Markdown',
                        disable_notification=True,
                        )
    
    # no such referral
    else:
        bot.send_message(chat_id=message.chat.id,
                        text=config.WRONG_REFERRAL_MESSAGE,
                        disable_notification=True,
                        )


@bot.message_handler(commands=['paid_all'])
def reduce_referrals_message(message):
    """Sets all referrals amount to 0."""

    # check permissions
    if str(message.from_user.id) in config.DIRECTOR_ID:
        bot.send_message(chat_id=message.chat.id,
                         text=config.REDUCE_BALANCE_MESSAGE,
                         reply_markup=keyboards.confirm_reduce_all_keyboard(),
                         disable_notification=True,
                         )
    
    # no permissions
    else:
        bot.send_message(chat_id=message.chat.id,
                        text=config.NO_PERMISSION_MESSAGE,
                        disable_notification=True,
                        )


@bot.message_handler(commands=['paid'])
def reduce_referrals_message(message):
    """Sets all referrals amount to 0."""

    # check permissions
    if str(message.from_user.id) in config.DIRECTOR_ID:
        referral = utils.extract_referral(message.text, '/paid')
        is_referral = functions.check_if_referral(referral)

        # if there is such referral
        if is_referral:
            # get referral information
            referral_info = functions.get_referral(referral)

            amount = utils.numbers_format(referral_info.amount)
            reply_text = f'Обнулить счет *{referral}* ({referral_info.identifier})? (текущий баланс счета *{amount}* бат.)'

            # ask confirmation to reduce the balance
            bot.send_message(chat_id=message.chat.id,
                            text=reply_text,
                            reply_markup=keyboards.confirm_reduce_keyboard(referral),
                            parse_mode='Markdown',
                            disable_notification=True,
                            )
        
        # no such referral
        else:
            bot.send_message(chat_id=message.chat.id,
                        text=config.WRONG_REFERRAL_MESSAGE,
                        disable_notification=True,
                        )
    
    # no permissions
    else:
        bot.send_message(chat_id=message.chat.id,
                        text=config.NO_PERMISSION_MESSAGE,
                        disable_notification=True,
                        )
        

@bot.message_handler(commands=['menu'])
def menu_message(message):
    """Displays menu without a large text."""

    bot.send_message(message.chat.id, 
                    text=config.MAIN_MENU_MESSAGE, 
                    parse_mode='Markdown',
                    reply_markup=keyboards.main_keyboard(),
                    disable_notification=True,
                    )
    

@bot.message_handler(commands=['rate'])
def rate_message(message):
    """Displays rate with menu button."""

    bot.send_message(message.chat.id, 
                    text=functions.currency_rate_message(), 
                    parse_mode='Markdown',
                    reply_markup=keyboards.menu_keyboard(),
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

    # if the query have relations with referral actions
    if query == 'referral':
        action = call_data[1]
        referral = call_data[2]

        # if user want's to get referral link and qr-code
        if action == 'info':
            # generate referral link based on referral
            bot.edit_message_text(message_id=message_id,
                                  chat_id=chat_id,
                                  text=f'Реферальная ссылка для {referral}: {config.BOT_LINK}?start={referral}',
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

            reply_text = f'Для резервирования реферала *{referral}* - в ответ на это сообщение укажите имя или название компании.'

            # ask for identifier as reply to the message
            bot.send_message(chat_id=chat_id,
                            text=reply_text,
                            reply_markup=telebot.types.ForceReply(input_field_placeholder='Имя/название компании'),
                            parse_mode='Markdown',
                            disable_notification=True,
                            )
        
        # if manager wants to register an exchange
        elif action == 'increase':
            # get exchange amount
            amount = float(call_data[3])

            # get referral object that contains all info needed
            referral_info = functions.get_referral(referral)

            # calculates the amount that should be on referral's account
            new_amount = round(referral_info.amount + amount * config.PROFIT_COEFF * config.REFERRAL_COEFF, 2)

            # change the referral balance amount
            functions.change_referral_amount(referral, new_amount)
            new_amount = utils.numbers_format(new_amount)

            bot.edit_message_text(message_id=message_id,
                                chat_id=chat_id,
                                text=f'Обмен пользователя учтен, на счету *{referral}* ({referral_info.identifier}) *{new_amount}* бат.',
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
                                text=config.REDUCED_BALANCE_MESSAGE,
                                )
                
            # reduce the referral balance to 0
            else:
                threading.Thread(daemon=True, 
                            target=functions.reduce_referral_balance, 
                            args=(referral,),
                            ).start()
                
                bot.edit_message_text(message_id=message_id,
                                chat_id=chat_id,
                                text=f'Баланс *{referral}* обнулен.',
                                parse_mode='Markdown',
                                )
    
    # cancel the action, deletes keyboard and changes message
    elif query == 'cancel':
        bot.edit_message_text(message_id=message_id,
                                chat_id=chat_id,
                                text=config.CANCEL_MESSAGE,
                                )     
        
    elif query == 'menu':
        bot.edit_message_reply_markup(chat_id=chat_id,
                                      message_id=message_id,
                                      reply_markup=telebot.types.InlineKeyboardMarkup(),
                                      )
        
        bot.send_message(chat_id=chat_id, 
                    text=config.MAIN_MENU_MESSAGE, 
                    parse_mode='Markdown',
                    reply_markup=keyboards.main_keyboard(),
                    disable_notification=True,
                    )
        
    elif query == 'exchanged':
        currency = call_data[1]
        exchange_type = call_data[2]

        bot.edit_message_reply_markup(chat_id=chat_id,
                                      message_id=message_id,
                                      reply_markup=keyboards.manager_application_keyboard(currency, exchange_type),
                                      )
        
        bot.send_message(chat_id=chat_id, 
                    text=config.MAIN_MENU_MESSAGE, 
                    parse_mode='Markdown',
                    reply_markup=keyboards.main_keyboard(),
                    disable_notification=True,
                    )
        
    elif query == 'sended':
        bot.edit_message_reply_markup(chat_id=chat_id,
                                      message_id=message_id,
                                      reply_markup=keyboards.only_manager_keyboard(),
                                      )
        
        bot.send_message(chat_id=chat_id, 
                    text=config.MAIN_MENU_MESSAGE, 
                    parse_mode='Markdown',
                    reply_markup=keyboards.main_keyboard(),
                    disable_notification=True,
                    )
    
    elif query == 'recalculate':
        currency = call_data[1]
        exchange_type = call_data[2]
        
        reply_text = f'''
                    \nНажмите кнопку *"{currency}"*, если хотите обменять определенную сумму в *{currency} на THB*.\
                    \n\
                    \nНажмите кнопку *"THB"*, если хотите получить определенную сумму в *THB* в обмен на *{currency}*.\
                    '''
        bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=reply_text,
                                parse_mode='Markdown',
                                )
        bot.edit_message_reply_markup(chat_id=chat_id,
                                        message_id=message_id,
                                        reply_markup=keyboards.amount_currency_keyboard(currency, exchange_type),
                                        )
        
    elif query == 'service':
        bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.SERVICE_MESSAGE,
                                  parse_mode='Markdown',
                                  )
        bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.service_keyboard(),
                                          )
    
    elif query == 'faq':
        bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.QUESTION_MESSAGE,
                                  parse_mode='Markdown',
                                  )
        bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.question_keyboard(),
                                          )
    
    elif query == 'atm':
        bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.ATM_MESSAGE,
                                  parse_mode='Markdown'
                                  )
        bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.atm_keyboard(query),
                                          )

    elif query == 'airport':
        bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.AIRPORT_MESSAGE,
                                  parse_mode='Markdown',
                                  )
        bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.back_faq_keyboard(query),
                                          )
        
    elif query == 'delivery':
        bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.DELIVERY_MESSAGE,
                                  parse_mode='Markdown',
                                  )
        bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.back_faq_keyboard(query),
                                          )
        
    elif query == 'transfer':
        bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.TRANSFER_MESSAGE,
                                  parse_mode='Markdown',
                                  )
        bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.back_faq_keyboard(query),
                                          )
        
    elif query == 'banks':
        bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.BANKS_MESSAGE,
                                  parse_mode='Markdown',
                                  )
        bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.only_back_keyboard(),
                                          )
    
    elif query == 'bangkok':
        try:
            bot.delete_message(chat_id, message_id)
        except:
            pass
        
        try:
            bot.send_document(chat_id=chat_id,
                            document=config.BANGKOK_FILE,
                            reply_markup=keyboards.back_atm_keyboard(),
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
                            reply_markup=keyboards.back_atm_keyboard(),
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
                          reply_markup=keyboards.back_atm_keyboard(),
                          )

    elif query == 'calculate':
        source = call_data[1]
        bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.PAIRS_MESSAGE,
                                  parse_mode='Markdown',
                                  )
        bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.pairs_keyboard(source),
                                          )

    elif query == 'exchange':
        currency = call_data[1]

        if len(call_data) == 2:
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.EXCHANGE_TYPE_MESSAGE,
                                  parse_mode='Markdown',
                                  )
            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.exchange_type_keyboard(currency),
                                          )
        
        elif len(call_data) == 3:
            exchange_type = call_data[2]
            
            if exchange_type != 'choose':
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
                                
                bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=reply_text,
                                    parse_mode='Markdown',
                                    )
                bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=keyboards.amount_currency_keyboard(currency, exchange_type),
                                            )
            else:
                bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text='Выберите подходящий район доставки:',
                                    parse_mode='Markdown',
                                    )
                bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=keyboards.delivery_types_keyboard(currency),
                                            )

        elif len(call_data) == 4:
            exchange_type = call_data[2]
            amount_currency = call_data[3]

            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except:
                pass

            translated_exchange_type = config.TYPE_RUSSIAN[exchange_type]
            minimal_amount = utils.numbers_format(config.TYPE_AMOUNT[exchange_type]).replace(' ', '.')

            reply_text = f'''
                    \nСпособ обмена: *{translated_exchange_type}*\
                    \nПара: *{currency}/THB*\
                    \n\
                    \nВ ответ на это сообщение введите сумму в *{amount_currency}* (*не менее {minimal_amount} THB*) для расчета актуального курса.\
                    '''
            bot.send_message(chat_id=chat_id,
                             text=reply_text,
                             reply_markup=telebot.types.ForceReply(input_field_placeholder=f'Сумма в {amount_currency}'),
                             parse_mode='Markdown',
                             disable_notification=True,
                             )
            
    elif query == 'send':
        user_message = call.message.text.replace(config.ADDITIONAL_MESSAGE, '')
        reply_text = 'Ваша заявка отправлена ✅\n\n' + user_message + 'Менеджер свяжется с вами в ближайшее время, также вы можете самостоятельно написать нашему менеджеру 👇'

        bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=reply_text,
                                  )
        bot.edit_message_reply_markup(chat_id=chat_id,
                                        message_id=message_id,
                                        reply_markup=keyboards.manager_keyboard(),
                                        )
        
        try:
            reply_text = f'Пользователь @{call.from_user.username} получил следующий расчет:\n\n' + user_message
            
            bot.send_message(chat_id=config.MANAGER_ID,
                        text=reply_text,
                        disable_notification=True,
                        )
        except:
            pass

    elif query == 'back':
        destination = call_data[1]

        if destination == 'main':
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.MAIN_MENU_MESSAGE,
                                  )
            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.main_keyboard(),
                                          )
        
        elif destination == 'faq':
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.QUESTION_MESSAGE,
                                  parse_mode='Markdown',
                                  )
            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.question_keyboard(),
                                          )
            
        elif destination == 'leave':
            try:
                bot.edit_message_reply_markup(chat_id=chat_id,
                                                message_id=message_id,
                                                reply_markup=telebot.types.InlineKeyboardMarkup(),
                                                )
            except:
                pass

            final_destination = call_data[2]

            if final_destination == 'main':
                bot.send_message(chat_id=chat_id, 
                    text=config.MAIN_MENU_MESSAGE, 
                    parse_mode='Markdown',
                    reply_markup=keyboards.main_keyboard(),
                    disable_notification=True,
                    )
                
            elif final_destination == 'atm':
                bot.send_message(chat_id=chat_id,
                                  text=config.ATM_MESSAGE,
                                  reply_markup=keyboards.atm_keyboard(final_destination),
                                  parse_mode='Markdown',
                                  disable_notification=True,
                                  )

        elif destination == 'pairs':
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.PAIRS_MESSAGE,
                                  parse_mode='Markdown',
                                  )
            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.pairs_keyboard('main'),
                                          )
            
        elif destination == 'type':
            currency = call_data[2]

            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.EXCHANGE_TYPE_MESSAGE,
                                  parse_mode='Markdown',
                                  )
            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.exchange_type_keyboard(currency),
                                          )
            
        elif destination == 'airport':
            bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=config.AIRPORT_MESSAGE,
                                    parse_mode='Markdown',
                                    )
            bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=keyboards.back_faq_keyboard(destination),
                                            )
            
        elif destination == 'delivery':
            bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=config.DELIVERY_MESSAGE,
                                    parse_mode='Markdown',
                                    )
            bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=keyboards.back_faq_keyboard(destination),
                                            )
            
        elif destination == 'transfer':
            bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=config.TRANSFER_MESSAGE,
                                    parse_mode='Markdown',
                                    )
            bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=keyboards.back_faq_keyboard(destination),
                                            )
            
        elif destination == 'banks':
            bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=config.BANKS_MESSAGE,
                                    parse_mode='Markdown',
                                    )
            bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=keyboards.back_faq_keyboard(destination),
                                            )
        
        elif destination == 'atm':
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=config.ATM_MESSAGE,
                                  parse_mode='Markdown'
                                  )
            bot.edit_message_reply_markup(chat_id=chat_id,
                                message_id=message_id,
                                reply_markup=keyboards.atm_keyboard(query),
                                )



@bot.message_handler(content_types=['text'])
def handle_text(message):
    """Handles message with type text. Gets identifier if user wants to add referral."""

    # check if the text is reply to a message with text that asks to enter identifier 
    # the "reply to" message should be sended by bot
    if (message.reply_to_message is not None) and\
    (config.CHECK_IDENTIFIER in message.reply_to_message.text) and\
    (str(message.reply_to_message.from_user.id) == config.BOT_ID):
        # delete "reply to" message to avoid reuse
        try:
            bot.delete_message(message.chat.id, message.reply_to_message.id)
        except:
            pass

        identifier = message.text
        unique_identifier = functions.check_unique_identifier(identifier)

        referral = utils.extract_referral_from_message(message.reply_to_message.text)

        # if the entered identifier is unique
        if unique_identifier:
            # add referral to database
            threading.Thread(daemon=True, 
                            target=functions.add_referral, 
                            args=(identifier, referral,),
                            ).start()
            
            reply_text = f'Реферал *{referral}* успешно зарезервирован.'

            bot.send_message(chat_id=message.chat.id,
                             text=reply_text,
                             parse_mode='Markdown',
                             disable_notification=True,
                             )
            
            user_id = message.from_user.id

            # generate qr-code
            functions.generate_qr(referral, user_id)

            # send referral link
            bot.send_message(chat_id=message.chat.id,
                            text=f'Реферальная ссылка для {referral}: {config.BOT_LINK}?start={referral}',
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
            reply_text = f'Такой идентификатор уже существует. Для резервирования реферала *{referral}* - в ответ на это сообщение укажите имя или название компании.'

            bot.send_message(chat_id=message.chat.id,
                            text=reply_text,
                            reply_markup=telebot.types.ForceReply(input_field_placeholder='Имя/название компании'),
                            parse_mode='Markdown',
                            disable_notification=True,
                            )
            
    elif (message.reply_to_message is not None) and\
    ('Способ обмена' in message.reply_to_message.text) and\
    ('Курс:' not in message.reply_to_message.text) and\
    (str(message.reply_to_message.from_user.id) == config.BOT_ID): 
        currency, exchange_type, amount_currency = utils.extract_exchange_info(message.reply_to_message.text)

        amount = utils.convert_to_float(message.text)
        translated_exchange_type = config.TYPE_RUSSIAN[exchange_type]
        minimal_amount = config.TYPE_AMOUNT[exchange_type]
        
        # if user entered a number
        if amount:
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
                exchange_rate = functions.get_exchange_rate(currency=currency,
                                                            delivery_type=exchange_type,
                                                            amount_currency=amount_currency,
                                                            amount=amount,
                                                            )
                
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
                
                currency_amount = utils.numbers_format(currency_amount)
                thb_amount = utils.numbers_format(thb_amount)

                # delete "reply to" message to avoid reuse (duplicated to avoid long waiting time for user between delete and answer)
                try:
                    bot.delete_message(message.chat.id, message.reply_to_message.id)
                except:
                    pass

                reply_text = f'''
                        \nСпособ обмена: *{translated_exchange_type}*\
                        \nПара: *{currency}/THB*\
                        \nКурс: *{exchange_rate}*\
                        \n\
                        \n*{currency_amount} {currency} ⏩ {thb_amount} THB*\
                        \n\
                        \n{config.ADDITIONAL_MESSAGE}\
                        '''
                
                bot.send_message(chat_id=message.chat.id,
                                text=reply_text,
                                reply_markup=keyboards.exchanged_keyboard(currency, exchange_type),
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

                reply_text = f'''
                        \nВведенная сумма эквивалента *{thb_amount} THB*, что меньше допустимого минимума в *{minimal_amount} THB* для выбранного способа обмена. Попробуйте еще раз.\
                        \n\
                        \nСпособ обмена: *{translated_exchange_type}*\
                        \nПара: *{currency}/THB*\
                        \n\
                        \nВ ответ на это сообщение введите сумму в *{amount_currency}* (*не менее {minimal_amount} THB*) для расчета актуального курса.\
                        '''
                
                bot.send_message(chat_id=message.chat.id,
                                text=reply_text,
                                reply_markup=telebot.types.ForceReply(input_field_placeholder=f'Сумма в {amount_currency}'),
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

            reply_text = f'''
                    \nВведенный ответ не является числом. Попробуйте еще раз.\
                    \n\
                    \nСпособ обмена: *{translated_exchange_type}*\
                    \nПара: *{currency}/THB*\
                    \n\
                    \nВ ответ на это сообщение введите сумму в *{amount_currency}* (*не менее {minimal_amount} THB*) для расчета актуального курса.\
                    '''
            bot.send_message(chat_id=message.chat.id,
                             text=reply_text,
                             reply_markup=telebot.types.ForceReply(input_field_placeholder=f'Сумма в {amount_currency}'),
                             parse_mode='Markdown',
                             disable_notification=True,
                             )

@bot.message_handler(content_types=['document'])
def handle_text(message):
    print(message)



if __name__ == '__main__':
    # bot.polling(timeout=80)
    while True:
        try:
            bot.polling()
        except:
            pass