import logging
import configparser

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from wakeonlan import wol
import qhue

import hue_lights

config = configparser.ConfigParser()


def init():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(funcName)s(): %(message)s')
    config.read('config.txt')
    start_updater()


def send_message(bot, update, text):
    """
        Sends a message only the auth-user, as configured in config.txt

        Params
        bot: Telegram bot object
        update: Telegram update object
        text: The text to say
    """
    auth_user_id = int(config.get('telegram', 'auth_user'))
    bot.send_message(chat_id=auth_user_id, text=text)


def check_authorised_user(func):
    def auth_check(bot, update):
        auth_user_id = int(config.get('telegram', 'auth_user'))
        current_user = update.message.from_user.id
        if auth_user_id == current_user:
            func(bot, update)
        else:
            bot.send_message(
                chat_id=auth_user_id,
                text='Unauthorised user request: %s %s | %s' %
                (update.message.from_user.first_name,
                    update.message.from_user.last_name,
                    update.message.text)
            )
            return False
    return auth_check


# Bot commands
@check_authorised_user
def start(bot, update):
    keyboard = [[
        InlineKeyboardButton('Lights on', callback_data='lights_on'),
        InlineKeyboardButton('Lights off', callback_data='lights_off')],
        [InlineKeyboardButton('Computer', callback_data='computer')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Hi Alan', reply_markup=reply_markup)


def callback_handler(bot, update):
    query = update.callback_query

    if query.data == 'lights_on':
        lights_response = hue_lights.lights_on()
        if lights_response:
            bot.answerCallbackQuery(query.id, text='Turning lights on...')
        else:
            bot.answerCallbackQuery(query.id, text='Lights are already on')
    elif query.data == 'lights_off':
        lights_response = hue_lights.lights_off()
        if lights_response:
            bot.answerCallbackQuery(query.id, text='Turning lights off...')
        else:
            bot.answerCallbackQuery(query.id, text='Lights are already off')
    elif query.data == 'computer':
        wol.send_magic_packet(config.get('computer', 'mac_address'))
        bot.answerCallbackQuery(query.id, text='Sending wake on LAN request')


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name)
    )


def start_updater():
    api_token = config.get('telegram', 'api_token')
    updater = Updater(api_token)
    updater.dispatcher.add_handler(CommandHandler('hey', start))
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback_handler))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    init()
