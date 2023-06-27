# Money exchange bot
## Изменить язык: [Русский](README.md)
***
A bilingual telegram bot for a currency exchanger that talks about the service and calculates real-time exchange rates based on Binance data. Added referral system.
## [DEMO](README.demo.md)
## [LIVE](https://t.me/@Change_money_bot)
## Functionality:
1. Navigation menu to answer the most popular questions
2. Notifications to the manager, if the user has left a request
3. An online calculator for calculating the exchange rate, which takes into account restrictions on the selected delivery method
4. Referral system for users
5. Generation of qr-codes for referrals
## Commands:
**For convenience, it is recommended to add these commands to the side menu of the bot using [BotFather](https://t.me/BotFather).**
- /menu - start menu;
- /rate - displays the current rates, taking into account the delivery method;
- /referral - a command that allows you to get your own referral link and qr-code by specifying any word that will be included in the referral link (eg /referral somebody);
- /exchange - a command available to the manager (MANAGER_ID), which indicates the nickname of the user who made the exchange and the amount of the exchange in THB (n/r /exchange someone 10000) - after entering the command, % of a certain amount is credited to the account of the referral from which he came user
- /balance - a command that displays the referral's balance to be paid (eg /balance somebody)
- /paid_all - a command that the director (DIRECTOR_ID) has access to, resets the current balance of all referrals
- /paid - a command that the director (DIRECTOR_ID) has access to, resets the current balance of the specified referral (eg /paid somebody)
- /all - command that the director (DIRECTOR_ID) has access to, displays all added referrals and their balance
## Installation and use:
- The config.py file contains variables with media files and documents to which the bot has access - you need to add your own:\
**BANGKOK_FILE**\
**KASIKORN_FILE**\
**KRUNGSRI_FILE**\
**REVIEWS_MEDIA_IMAGES**
- The config.py file contains variables that you need to customize according to your needs:\
**MANAGER_ID** (this user is being notified,)\
**MANAGER_USERNAME** (manager's nickname in telegram)\
**BOT_ID** (numbers in bot token)\
**DIRECTOR_ID** (this user has access to execute all commands)\
**BOT_LINK** (link to bot)\
**TG_CHANNEL** (link to telegram channel)\
**INSTAGRAM** (link to instagram)
> To determine the user ID, you need to send any message from the corresponding account to the next [bot] (https://t.me/getmyid_bot). The value contained in **Your user ID** - the user ID
- Logging will be entered into the py_log.log file in case of errors;
- Create an .env file containing the following variables:
> the file is created in the root folder of the project
   - specify the bot's telegram token in the file:\
   **TELEGRAM_TOKEN**=TOKEN
- Install the virtual environment and activate it (if necessary):
> Installation and activation in the root folder of the project
```sh
python3 -m venv venv
source venv/bin/activate # for macOS
source venv/Scripts/activate # for Windows
```
- Install dependencies:
```sh
pip install -r requirements.txt
```
- Run project:
```sh
python3 main.py
```