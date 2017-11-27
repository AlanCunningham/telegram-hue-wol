import logging
import configparser

from telegram.ext import Updater, CommandHandler
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
                    update.message.text
                )
            )
            return False
    return auth_check


# Bot commands
@check_authorised_user
def start(bot, update):
    update.message.reply_text('Hi Alan!')


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name)
    )


@check_authorised_user
def wake_computer(bot, update):
    wol.send_magic_packet(config.get('computer', 'mac_address'))
    update.message.reply_text('Sending wake on lan request')


@check_authorised_user
def lights_on(bot, update):
    lights_action = hue_lights.lights_on(update)
    if lights_action:
        response_message = 'Turning lights on...'
    else:
        response_message = 'Lights are already on'
    send_message(bot, update, response_message)


@check_authorised_user
def lights_off(bot, update):
    lights_action = hue_lights.lights_off(update)
    if lights_action:
        response_message = 'Turning lights off...'
    else:
        response_message = 'Lights are already off'
    send_message(bot, update, response_message)


def start_updater():
    api_token = config.get('telegram', 'api_token')
    updater = Updater(api_token)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('computer', wake_computer))
    updater.dispatcher.add_handler(CommandHandler('lightson', lights_on))
    updater.dispatcher.add_handler(CommandHandler('lightsoff', lights_off))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    init()
